import telebot
from telebot import types
import requests
import os

# --- tokens & config from environment (safer) ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
FLASK_URL = os.getenv("FLASK_URL", "https://otp-bot-production-a1ce.up.railway.app")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📞 Call Client"),
        types.KeyboardButton("🔐 Send OTP"),
        types.KeyboardButton("📜 View Logs"),
        types.KeyboardButton("⚙️ Help")
    )
    bot.send_message(
        message.chat.id,
        "💼 *Control Panel*\nChoose an action below:",
        reply_markup=markup,
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda msg: True)
def handle_buttons(message):
    text = message.text.strip()

    if text == "📞 Call Client":
        bot.send_message(message.chat.id, "Enter client number in international format (e.g. +15551234567):")
        bot.register_next_step_handler(message, make_call)

    elif text == "🔐 Send OTP":
        bot.send_message(message.chat.id, "OTP trigger sent ✅ (logic can be added later).")

    elif text == "📜 View Logs":
        bot.send_message(message.chat.id, "Fetching logs… (endpoint coming soon).")

    elif text == "⚙️ Help":
        bot.send_message(message.chat.id, "Use the buttons to control calls, OTPs, and logs.\n/start to reopen menu.")

    else:
        bot.send_message(message.chat.id, "Command not recognized.\nUse /start to reopen the menu.")


def make_call(message):
    number = message.text.strip()
    if not number.startswith("+"):
        bot.send_message(message.chat.id, "❌ Please include international prefix (e.g. +1...).")
        return
    try:
        r = requests.post(f"{FLASK_URL}/call-client", json={"to": number}, timeout=10)
        if r.status_code == 200:
            bot.send_message(message.chat.id, f"📞 Calling {number}...")
        else:
            bot.send_message(message.chat.id, f"⚠️ Failed: {r.text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


if __name__ == "__main__":
    print(">>> Telegram bot started")
    bot.infinity_polling(skip_pending=True)