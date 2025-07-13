from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

# Change this to your actual middleware/chatbot endpoint
MIDDLEWARE_CHAT_URL = "https://server-py-ebxq.onrender.com/chat"

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')

    print(f"[WhatsApp] {sender} said: {incoming_msg}")

    # Call your chatbot backend
    try:
    response = requests.post(MIDDLEWARE_CHAT_URL, json={"message": incoming_msg}, timeout=5)
    print("Middleware status:", response.status_code)
    print("Middleware response text:", response.text)

    rasa_messages = response.json()

    if isinstance(rasa_messages, list) and rasa_messages:
        bot_reply = rasa_messages[0].get("text", "Sorry, I couldn’t understand that.")
    elif isinstance(rasa_messages, dict) and "reply" in rasa_messages:
        bot_reply = rasa_messages["reply"]
    else:
        bot_reply = "Sorry, I couldn’t understand that."
        
except Exception as e:
    print("Error talking to chatbot middleware:", e)
    bot_reply = "Sorry, something went wrong."

    # Respond to WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)


port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
