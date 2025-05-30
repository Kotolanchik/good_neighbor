# bot/facade.py

from telebot import TeleBot
from utils.bot.keyboard_utils import create_reply_keyboard, create_inline_keyboard
from utils.bot.menu_utils import create_menu_options

class BotFacade:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def send_message_with_reply_keyboard(self, chat_id, text, buttons):
        """
        Отправляет сообщение с reply-клавиатурой.
        """
        keyboard = create_reply_keyboard(buttons)
        self.bot.send_message(chat_id, text, reply_markup=keyboard)

    def send_message_with_inline_keyboard(self, chat_id, text, options):
        """
        Отправляет сообщение с inline-клавиатурой.
        """
        buttons = create_menu_options(options)
        keyboard = create_inline_keyboard([buttons])
        self.bot.send_message(chat_id, text, reply_markup=keyboard)

    def handle_callback_query(self, call):
        """
        Обрабатывает callback-запросы от inline-кнопок.
        """
        self.bot.answer_callback_query(call.id)
        self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   text=f"Вы выбрали: {call.data}")