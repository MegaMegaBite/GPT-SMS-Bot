from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "GPT SMS Bot is running."

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}],
            temperature=0.7
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        reply_text = f"Error: {str(e)}"

    twilio_reply = MessagingResponse()
    twilio_reply.message(reply_text)
    return str(twilio_reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
