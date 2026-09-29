import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def verify_openrouter():
    print("Testing OpenRouter Handshake...")
    if not OPENROUTER_API_KEY or "your_" in OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY is not set correctly in .env.")
        return

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "SoulMi"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo", # using a standard cheap model for handshake
        "messages": [{"role": "user", "content": "Say 'Handshake successful' if you can hear me."}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            print(f"[SUCCESS] OpenRouter Handshake Successful! Response: {reply}")
        else:
            print(f"[FAILED] OpenRouter Handshake Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

if __name__ == "__main__":
    verify_openrouter()
