# app.py
from flask import Flask, request
import requests
import openai

# === CONFIG ===
TELEGRAM_BOT_TOKEN = "7899622099:AAGfW6kGkbJ1Gh7NEiN2zHhOvLEsw38vdQk"
OPENAI_API_KEY = "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"
ALLOWED_USER_IDS = [123456789, 987654321]  # Danh sách user ID được phép

# === SETUP ===
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

def chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response['choices'][0]['message']['content']

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "")

    if user_id not in ALLOWED_USER_IDS:
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": "❌ Bạn chưa được cấp quyền sử dụng bot này. Vui lòng liên hệ admin."
        })
        return {"ok": True}

    reply = chatgpt_response(text)
    requests.post(TELEGRAM_API_URL, json={
        "chat_id": chat_id,
        "text": reply
    })
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
