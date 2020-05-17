import os
import telegram

def send_telegram_message(chat_id, message):
    token = os.environ.get('TELEGRAM_TOKEN', None)
    bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=message)