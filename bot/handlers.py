from bot.facade import BotFacade
from bot.keyboards import create_start_keyboard
from bot.messages import WELCOME_TEXT, FAQ_TEXT
from bot.chain_message.create_user import create_profile

def register_handlers(bot):
    facade = BotFacade(bot)

    @bot.message_handler(commands=['start'])
    def start_handler(message):
        keyboard = create_start_keyboard()
        bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        create_profile(call.messagge)

