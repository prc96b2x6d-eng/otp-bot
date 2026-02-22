from twilio.rest import Client
import os
from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route('/call-client', methods=['POST'])
def call_client():
    try:
        data = request.get_json()
        number = data.get("to")

        if not number:
            return jsonify({"error": "Missing phone number"}), 400

        # pull env vars from Railway dashboard
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to=number,
            from_=twilio_number,
            url="https://otp-bot-production-a1ce.up.railway.app/voice"  # TwiML callback
        )

        return jsonify({"status": "calling", "sid": call.sid}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
