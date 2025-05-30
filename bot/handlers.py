from bot.facade import BotFacade
from bot.keyboards import create_start_keyboard
from bot.messages import WELCOME_TEXT, FAQ_TEXT

def register_handlers(bot):
    facade = BotFacade(bot)

    @bot.message_handler(commands=['start'])
    def start_handler(message):
        keyboard = create_start_keyboard()
        bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        facade.bot.answer_callback_query(call.id)
        if call.data == "edit_card":
            facade.send_message(call.message.chat.id, "Здесь можно редактировать карточку.")
        elif call.data == "find_help":
            facade.send_message(call.message.chat.id, "Поиск помощи запущен...")
        elif call.data == "my_rating":
            facade.send_message(call.message.chat.id, "Ваш рейтинг: 5")
        elif call.data == "help_faq":
            facade.send_message(call.message.chat.id, FAQ_TEXT)
        else:
            facade.send_message(call.message.chat.id, f"Вы выбрали: {call.data}")
