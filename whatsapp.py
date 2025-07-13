from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

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
        response = requests.post(MIDDLEWARE_CHAT_URL, json={"message": incoming_msg})
        bot_reply = response.json().get("reply", "Sorry, I couldn’t understand that.")
    except Exception as e:
        print("Error talking to chatbot middleware:", e)
        bot_reply = "Sorry, something went wrong."

    # Respond to WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
