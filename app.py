from flask import Flask, request
import requests
import openai

# === CONFIG ===
TELEGRAM_BOT_TOKEN = "7899622099:AAGfW6kGkbJ1Gh7NEiN2zHhOvLEsw38vdQk"
OPENAI_API_KEY = "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"
ALLOWED_USER_IDS = [123456789, 987654321]  # Cập nhật user ID thật của bạn tại đây

# === SETUP ===
TELEGRAM_API_URL = f"https://api.telegram.org/bot7899622099:AAGfW6kGkbJ1Gh7NEiN2zHhOvLEsw38vdQk/sendMessage"
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

def chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("🔥 LỖI GPT:", e)
        return "❌ Lỗi khi xử lý với ChatGPT."

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📥 Nhận request từ Telegram:", data)  # Log toàn bộ request

        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        user_id = message.get("from", {}).get("id")
        text = message.get("text", "")

        print(f"🧾 User ID: {user_id} | Nội dung: {text}")

        if user_id not in ALLOWED_USER_IDS:
            print("🚫 User không có trong whitelist. Từ chối truy cập.")
            requests.post(TELEGRAM_API_URL, json={
                "chat_id": chat_id,
                "text": "❌ Bạn chưa được cấp quyền sử dụng bot này. Vui lòng liên hệ admin."
            })
            return {"ok": True}

        reply = chatgpt_response(text)
        print("✅ Trả lời từ GPT:", reply)

        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": reply
        })
        return {"ok": True}

    except Exception as e:
        print("💥 LỖI webhook:", e)
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
