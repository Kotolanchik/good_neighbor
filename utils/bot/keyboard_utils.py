# utils/keyboard_utils.py

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def create_reply_keyboard(buttons, one_time_keyboard=False, resize_keyboard=True):
    """
    Создает клавиатуру с кнопками.
    :param buttons: Список списков кнопок.
    :param one_time_keyboard: Удалять клавиатуру после использования.
    :param resize_keyboard: Автоматически изменять размер клавиатуры.
    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardMarkup(one_time_keyboard=one_time_keyboard, resize_keyboard=resize_keyboard)
    for row in buttons:
        markup.row(*[KeyboardButton(button) for button in row])
    return markup


def create_inline_keyboard(buttons):
    """
    Создает inline-клавиатуру.
    :param buttons: Список кортежей (текст кнопки, callback_data).
    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    for row in buttons:
        markup.row(*[InlineKeyboardButton(text, callback_data=data) for text, data in row])
    return markup
