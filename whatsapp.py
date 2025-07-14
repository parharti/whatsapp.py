from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

# ✅ Your deployed middleware URL
MIDDLEWARE_CHAT_URL = "https://server-py-ebxq.onrender.com/chat"

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '').replace("whatsapp:", "").strip()

    print(f"[WhatsApp] {sender} said: {incoming_msg}")

    try:
        # ✅ Prepare payload exactly as server.py expects
        payload = {
            "message": incoming_msg,
            "sender": sender
        }

        response = requests.post(MIDDLEWARE_CHAT_URL, json=payload, timeout=10)
        print("[Middleware] Status:", response.status_code)
        print("[Middleware] Raw response:", response.text)

        rasa_response = response.json()

        # ✅ Extract message from standard Rasa REST response
        if isinstance(rasa_response, list) and rasa_response:
            messages = [msg.get("text") for msg in rasa_response if "text" in msg]
            bot_reply = "\n".join(messages) if messages else "I didn’t get a reply from the bot."
        else:
            bot_reply = "I didn’t get a valid response from the bot."

    except Exception as e:
        print("[Error] Chatbot middleware failed:", e)
        bot_reply = "Oops! Something went wrong talking to the bot."

    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
