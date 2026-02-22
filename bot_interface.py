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
        account_sid = os.getenv("ACd8d664da758592de1294c800a4b25fee")
        auth_token = os.getenv("bdd85100bb9925f0a1aefd1ef21748f6")
        twilio_number = os.getenv("+16572864747")

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to=number,
            from_=twilio_number,
            url="https://otp-bot-production-a1ce.up.railway.app/voice"  # TwiML callback
        )

        return jsonify({"status": "calling", "sid": call.sid}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
