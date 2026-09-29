import base64
import os
from datetime import datetime
 
import numpy as np
import cv2
import requests as upstream_requests
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
 
from db import get_connection
from emotion_model import detect_faces_and_emotions, active_model_kind
 
load_dotenv()
 
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
 
# Allow the frontend (Live Server, usually port 5500) to call this API with cookies
CORS(app, supports_credentials=True, origins=[os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500")])
 
# Interactive API docs, Flask's equivalent of FastAPI's /docs — browse to
# http://127.0.0.1:5000/apidocs once the server is running.
app.config["SWAGGER"] = {"title": "SoulMi API", "uiversion": 3}
Swagger(app, template={
    "info": {
        "title": "SoulMi API",
        "description": "Auth, mood tracking, facial-expression detection, and the AI chat proxy.",
        "version": "1.0.0",
    },
})
 
 
# ---------- Auth ----------
 
@app.route("/api/signup", methods=["POST"])
def signup():
    """Create an account
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, email, password]
          properties:
            name: {type: string, example: "Priya"}
            email: {type: string, example: "priya@example.com"}
            password: {type: string, example: "hunter2"}
    responses:
      201: {description: Account created}
      400: {description: Missing fields}
      409: {description: Email already registered}
    """
    data = request.get_json(force=True)
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
 
    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400
 
    password_hash = generate_password_hash(password)
 
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, password_hash),
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
    except Exception as e:
        conn.rollback()
        if "Duplicate entry" in str(e):
            return jsonify({"error": "An account with this email already exists"}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
 
    session["user_id"] = user_id
    return jsonify({"message": "Account created", "user_id": user_id}), 201
 
 
@app.route("/api/login", methods=["POST"])
def login():
    """Log in
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email: {type: string, example: "priya@example.com"}
            password: {type: string, example: "hunter2"}
    responses:
      200: {description: Logged in, session cookie set}
      401: {description: Invalid email or password}
    """
    data = request.get_json(force=True)
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
 
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
    finally:
        conn.close()
 
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401
 
    session["user_id"] = user["id"]
    return jsonify({"message": "Logged in", "user_id": user["id"], "name": user["name"]})
 
 
@app.route("/api/logout", methods=["POST"])
def logout():
    """Log out
    ---
    tags: [Auth]
    responses:
      200: {description: Session cleared}
    """
    session.clear()
    return jsonify({"message": "Logged out"})
 
 
def current_user_id():
    return session.get("user_id")
 
 
# ---------- Mood tracking ----------
 
@app.route("/api/mood", methods=["POST"])
def log_mood():
    """Log a mood entry (requires login)
    ---
    tags: [Mood]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [emotion]
          properties:
            emotion: {type: string, example: "happy"}
            confidence: {type: number, example: 0.9}
            note: {type: string, example: "manual check-in"}
    responses:
      201: {description: Mood logged}
      401: {description: Not logged in}
    """
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
 
    data = request.get_json(force=True)
    emotion = data.get("emotion")
    confidence = data.get("confidence")
    note = data.get("note", "")
 
    if not emotion:
        return jsonify({"error": "emotion is required"}), 400
 
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mood_entries (user_id, detected_emotion, confidence, note) VALUES (%s, %s, %s, %s)",
            (user_id, emotion, confidence, note),
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()
 
    return jsonify({"message": "Mood logged"}), 201
 
 
@app.route("/api/mood-history", methods=["GET"])
def mood_history():
    """Get the logged-in user's last 100 mood entries
    ---
    tags: [Mood]
    responses:
      200: {description: List of mood entries}
      401: {description: Not logged in}
    """
    user_id = current_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
 
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT id, detected_emotion, confidence, note, recorded_at
               FROM mood_entries WHERE user_id = %s
               ORDER BY recorded_at DESC LIMIT 100""",
            (user_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
    finally:
        conn.close()
 
    for row in rows:
        row["recorded_at"] = row["recorded_at"].isoformat()
 
    return jsonify(rows)
 
 
# ---------- Facial-expression mood detection ----------
 
@app.route("/api/detect-mood", methods=["POST"])
def detect_mood():
    """Detect emotion from a webcam frame
    ---
    tags: [Mood]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [image]
          properties:
            image:
              type: string
              description: base64 data URL, e.g. "data:image/jpeg;base64,..."
    responses:
      200: {description: Detected emotion (or faces_found 0 if no face)}
      400: {description: Invalid/missing image}
      503: {description: Model weights not downloaded yet}
    """
    data = request.get_json(force=True)
    image_data_url = data.get("image", "")
    if not image_data_url:
        return jsonify({"error": "image is required"}), 400
 
    if "," in image_data_url:
        image_data_url = image_data_url.split(",", 1)[1]
 
    try:
        img_bytes = base64.b64decode(image_data_url)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        bgr_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if bgr_image is None:
            raise ValueError("could not decode image bytes")
    except Exception as e:
        return jsonify({"error": f"Invalid image data: {e}"}), 400
 
    try:
        results = detect_faces_and_emotions(bgr_image, max_faces=1)
    except FileNotFoundError as e:
        # Pretrained/fine-tuned weights haven't been downloaded yet
        return jsonify({"error": str(e)}), 503
 
    if not results:
        return jsonify({
            "faces_found": 0,
            "message": "No face detected — try better lighting or move closer to the camera.",
        }), 200
 
    top = results[0]
 
    logged = False
    user_id = current_user_id()
    if user_id:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mood_entries (user_id, detected_emotion, confidence, note) "
                "VALUES (%s, %s, %s, %s)",
                (user_id, top["emotion"], top["confidence"], "auto-detected via webcam"),
            )
            conn.commit()
            cursor.close()
            logged = True
        finally:
            conn.close()
 
    return jsonify({
        "faces_found": len(results),
        "emotion": top["emotion"],
        "confidence": top["confidence"],
        "scores": top["scores"],
        "box": top["box"],
        "model": active_model_kind(),
        "logged_to_history": logged,
    })
 
 
# ---------- AI chat (server-side OpenRouter proxy) ----------
 
SOULMI_SYSTEM_PROMPT = """You are SoulMi AI, a warm, compassionate, and deeply empathetic mental health companion. You are NOT a replacement for professional therapy — you are a supportive friend who listens without judgment.
 
Your personality:
- Warm, gentle, and caring — like a trusted friend
- You validate feelings before offering perspective
- You use simple, heartfelt language (avoid clinical jargon)
- You ask thoughtful follow-up questions to understand better
- You suggest grounding exercises, breathing techniques, or journaling when appropriate
- You gently recommend professional help when situations seem serious
- Keep responses concise (2-4 sentences usually) but meaningful
- Use occasional emojis sparingly (💛, 🌱, 🤗) to feel human
 
Important rules:
- Never diagnose conditions or prescribe medication
- Never minimize someone's feelings
- If someone mentions self-harm or suicide, immediately provide crisis resources (988 Suicide & Crisis Lifeline, or local emergency services) and encourage them to reach out
- Always remind users that they are not alone"""
 
 
@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat with the SoulMi AI (server-side OpenRouter proxy)
    ---
    tags: [Chat]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            prompt: {type: string, example: "I'm feeling anxious today"}
            messages:
              type: array
              items: {type: object}
              description: Full [{role, content}, ...] history — use instead of prompt for multi-turn.
            include_mood_context:
              type: boolean
              description: Splice the user's real MySQL mood history into the system prompt.
    responses:
      200: {description: "{reply: string}"}
      400: {description: Missing prompt/messages}
      502: {description: OpenRouter error}
      503: {description: OPENROUTER_API_KEY not configured}
    """
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return jsonify({"error": "OPENROUTER_API_KEY is not configured on the server"}), 503
 
    data = request.get_json(force=True)
    messages = data.get("messages")
    prompt = data.get("prompt")
    system_prompt = data.get("system_prompt") or SOULMI_SYSTEM_PROMPT
    max_tokens = int(data.get("max_tokens", 300))
    temperature = float(data.get("temperature", 0.8))
    include_mood_context = bool(data.get("include_mood_context", False))
 
    if not messages:
        if not prompt:
            return jsonify({"error": "messages or prompt is required"}), 400
        messages = [{"role": "user", "content": prompt}]
 
    final_system_prompt = system_prompt
    if include_mood_context:
        user_id = current_user_id()
        if user_id:
            conn = get_connection()
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    """SELECT detected_emotion, confidence, recorded_at FROM mood_entries
                       WHERE user_id = %s ORDER BY recorded_at DESC LIMIT 7""",
                    (user_id,),
                )
                rows = cursor.fetchall()
                cursor.close()
            finally:
                conn.close()
 
            if rows:
                lines = "\n".join(
                    f"- {r['recorded_at'].strftime('%Y-%m-%d %H:%M')}: {r['detected_emotion']}"
                    + (f" ({r['confidence']:.0%} confidence)" if r["confidence"] else "")
                    for r in rows
                )
                final_system_prompt += (
                    "\n\n[USER RECORD DATA]\nThe user has opted to share their real mood history "
                    "with you, logged from manual check-ins and webcam facial-expression detection. "
                    "If you reference this data, start that sentence with the exact phrase: "
                    '"Based on the records you stored...". Do NOT mention journal entries — you '
                    "don't have access to those (kept private/encrypted).\n\n"
                    f"Recent mood entries (most recent first):\n{lines}"
                )
 
    non_system = [m for m in messages if m.get("role") != "system"]
    outgoing = [{"role": "system", "content": final_system_prompt}] + non_system[-11:]
 
    try:
        resp = upstream_requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500"),
                "X-Title": "SoulMi AI Companion",
            },
            json={
                "model": os.getenv("OPENROUTER_MODEL", "openrouter/free"),
                "messages": outgoing,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
            },
            timeout=30,
        )
    except upstream_requests.RequestException as e:
        return jsonify({"error": f"Could not reach the AI provider: {e}"}), 502
 
    if resp.status_code != 200:
        return jsonify({"error": "AI provider error", "detail": resp.text}), 502
 
    body = resp.json()
    reply = ((body.get("choices") or [{}])[0].get("message", {}) or {}).get("content", "").strip()
    if not reply:
        reply = "I'm here for you. Could you tell me more about what's on your mind?"
 
    return jsonify({"reply": reply})
 
 
@app.route("/api/health", methods=["GET"])
def health():
    """Health check
    ---
    tags: [System]
    responses:
      200: {description: "{status: ok, time: ...}"}
    """
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})
 
 
if __name__ == "__main__":
    app.run(debug=True, port=5000)