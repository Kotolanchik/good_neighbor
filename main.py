import os

from telebot import TeleBot
from bot.handlers import register_handlers
from dotenv import load_dotenv
from db.database import conn
from bot.handlers import register_handlers


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(TOKEN)

register_handlers(bot,conn)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
