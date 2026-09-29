# Mental Wellness Backend (Flask + MySQL)

## 1. Install MySQL locally
If you don't have it yet: install **MySQL Community Server** + **MySQL Workbench** from mysql.com.

## 2. Create the database
Open MySQL Workbench (or the `mysql` CLI) and run everything in `schema.sql`. This creates the
`mental_wellness_db` database and all four tables (users, mood_entries, journal_entries, wellness_activities).

## 3. Set up the Python environment
In VS Code, open a terminal in this `backend` folder:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

## 4. Configure your credentials
Copy `.env.example` to `.env` and fill in your real MySQL password:

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # Mac/Linux
```

Edit `.env` and set `MYSQL_PASSWORD` to whatever you set when installing MySQL.

## 5. Run the server
```bash
python app.py
```

You should see it running on `http://127.0.0.1:5000`. Test it's alive by visiting
`http://127.0.0.1:5000/api/health` in your browser — you should get back `{"status": "ok", ...}`.

## 6. Run the frontend alongside it
Keep your `soulmi-main` site running on Live Server (port 5500) like before. Both run at the same time —
Live Server serves the HTML/CSS/JS, Flask serves the API. Your frontend JS will call
`http://127.0.0.1:5000/api/...` endpoints.

## Available endpoints
- `POST /api/signup` — {name, email, password}
- `POST /api/login` — {email, password}
- `POST /api/logout`
- `POST /api/mood` — {emotion, confidence, note} (requires login)
- `GET /api/mood-history` — returns last 100 mood entries for the logged-in user
- `POST /api/detect-mood` — {image: "data:image/jpeg;base64,..."} — runs the webcam frame through
  the facial-expression model and returns the detected emotion. Auto-logs to `mood_entries` if
  the caller is logged in.
- `POST /api/chat` — {messages: [...]} or {prompt: "..."}, optional `include_mood_context: true`
  — proxies to OpenRouter server-side so the API key stays out of the browser, optionally
  enriching the system prompt with the user's real mood history from MySQL.
- `GET /api/health` — quick check the server is up

## 7. Set up facial-expression mood detection
The model code is already written (`emotion_model.py`, `download_pretrained_model.py`,
`train_emotion_model.py`) — you just need weights:

```bash
python download_pretrained_model.py
```

This grabs a public pretrained FER2013 mini-XCEPTION checkpoint, good enough to demo
`/api/detect-mood` immediately. To actually fine-tune it (recommended for a real project,
since it improves accuracy on your own webcam/lighting conditions vs. the generic weights):

```bash
# 1. Put labelled face images under data/train/<emotion>/ and data/val/<emotion>/
#    (emotions: angry, disgust, fear, happy, sad, surprise, neutral)
# 2. Run the fine-tune
python train_emotion_model.py --epochs 15 --freeze-base
```

The fine-tuned weights are picked up automatically over the generic ones — no code changes
needed, just restart the server.

## 8. Set up the chatbot
Copy an OpenRouter API key into `.env` as `OPENROUTER_API_KEY` (get one free at
openrouter.ai/keys). The frontend no longer needs — or should have — an API key of its own;
all chat requests are proxied through `/api/chat`.
