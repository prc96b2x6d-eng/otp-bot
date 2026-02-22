import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
FLASK_URL = "https://otp-bot-production-a1ce.up.railway.app"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Bot is live. Send a number to call.")

@bot.message_handler(func=lambda m: True)
def handle_number(msg):
    num = msg.text.strip()
    try:
        r = requests.post(f"{FLASK_URL}/call-client", json={"to": num})
        if r.status_code == 200:
            bot.reply_to(msg, "📞 Calling...")
        else:
            bot.reply_to(msg, f"Error: {r.text}")
    except Exception as e:
        bot.reply_to(msg, f"Error: {e}")

if __name__ == "__main__":
    print("TeleBot: polling started")
    bot.polling(none_stop=True)