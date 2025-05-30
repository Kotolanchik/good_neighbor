from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class BotFacade:
    def __init__(self, bot):
        self.bot = bot

    def send_inline_keyboard(self, chat_id, text, buttons):
        keyboard = InlineKeyboardMarkup(row_width=1)
        for text_btn, callback in buttons:
            keyboard.add(InlineKeyboardButton(text_btn, callback_data=callback))
        self.bot.send_message(chat_id, text, reply_markup=keyboard)

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id, text)
