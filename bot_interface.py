import telebot
from telebot import types
import requests

BOT_TOKEN = "8510534078:AAGtu385CrVKNWURkvxnIhdmHw1E_dvqgmM"
bot = telebot.TeleBot(BOT_TOKEN)

# --- your Flask server endpoint ---
FLASK_URL = "https://otp-bot-production-a1ce.up.railway.app"


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    call_btn = types.KeyboardButton("📞 Call Client")
    otp_btn = types.KeyboardButton("🔐 Send OTP")
    logs_btn = types.KeyboardButton("📜 View Logs")
    help_btn = types.KeyboardButton("⚙️ Help")

    markup.add(call_btn, otp_btn, logs_btn, help_btn)
    bot.send_message(message.chat.id,
                     "💼 *Control Panel*\nChoose an action below:",
                     reply_markup=markup,
                     parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def handle_buttons(message):
    text = message.text

    if text == "📞 Call Client":
        bot.send_message(message.chat.id, "Enter the client’s number in international format (e.g. +15551234567):")
        bot.register_next_step_handler(message, make_call)

    elif text == "🔐 Send OTP":
        bot.send_message(message.chat.id, "OTP Trigger Sent ✅ (you can hook logic later).")

    elif text == "📜 View Logs":
        bot.send_message(message.chat.id, "Fetching logs... (link coming soon).")

    elif text == "⚙️ Help":
        bot.send_message(message.chat.id, "Use the buttons to control calls, OTPs, and logs. /start to reopen menu.")

    else:
        bot.send_message(message.chat.id, "Command not recognized. Use /start to reopen the menu.")


def make_call(message):
    number = message.text.strip()
    data = {"to": number}
    try:
        r = requests.post(f"{FLASK_URL}/call-client", json=data)
        if r.status_code == 200:
            bot.send_message(message.chat.id, f"📞 Calling {number}...")
        else:
            bot.send_message(message.chat.id, f"⚠️ Failed: {r.text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


bot.infinity_polling()