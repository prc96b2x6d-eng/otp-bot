from twilio.rest import Client
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/call-client', methods=['POST'])
def call_client():
    try:
        data = request.get_json()
        number = data.get("to")
        if not number:
            return jsonify({"error": "Missing phone number"}), 400

        # correct: pull from env vars (names, not values)
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            to=number,
            from_=twilio_number,
            url="https://otp-bot-production-a1ce.up.railway.app/voice",
            status_callback="https://otp-bot-production-a1ce.up.railway.app/status-callback",
            status_callback_event=["ringing", "in-progress", "completed"]
        )

        return jsonify({"status": "calling", "sid": call.sid}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)