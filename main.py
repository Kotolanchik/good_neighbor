# bot/main.py
import os

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message
from bot.facade import BotFacade

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = TeleBot(BOT_TOKEN)
facade = BotFacade(bot)

@bot.message_handler(commands=["start"])
def start(message: Message):
    """
    Команда /start.
    """
    buttons = [["Кнопка 1", "Кнопка 2"], ["Кнопка 3"]]
    facade.send_message_with_reply_keyboard(message.chat.id, "Выберите действие:", buttons)

@bot.message_handler(commands=["menu"])
def menu(message: Message):
    """
    Команда /menu.
    """
    options = ["Опция 1", "Опция 2", "Опция 3"]
    facade.send_message_with_inline_keyboard(message.chat.id, "Выберите опцию:", options)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """
    Обработка callback-запросов.
    """
    facade.handle_callback_query(call)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)