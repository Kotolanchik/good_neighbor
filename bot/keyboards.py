from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_start_keyboard():
    buttons = [
        ("Создать/редактировать карточку", "edit_card"),
        ("Найти помощь", "find_help"),
        ("Посмотреть мой рейтинг", "my_rating"),
        ("Помощь / FAQ", "help_faq"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    for text, callback in buttons:
        keyboard.add(InlineKeyboardButton(text, callback_data=callback))
    return keyboard
