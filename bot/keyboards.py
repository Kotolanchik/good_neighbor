from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def create_start_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("Создать/редактировать карточку", callback_data="edit_card"),
        InlineKeyboardButton("Найти помощь", callback_data="find_help"),
        InlineKeyboardButton("Посмотреть мой рейтинг", callback_data="my_rating"),
        InlineKeyboardButton("Помощь / FAQ", callback_data="help_faq"),
    ]
    markup.add(*buttons)
    return markup

def create_skills_keyboard(skills, selected_skills=None):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for skill_id, skill_name in skills:
        if selected_skills and skill_id in selected_skills:
            button_text = f"✅ {skill_name}"
        else:
            button_text = skill_name
        callback_data = f"skill_{skill_id}"
        keyboard.add(InlineKeyboardButton(button_text, callback_data=callback_data))
    keyboard.add(InlineKeyboardButton("Готово", callback_data="skills_done"))
    return keyboard

def create_gender_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Мужской", callback_data="gender_male"))
    markup.add(InlineKeyboardButton("Женский", callback_data="gender_female"))
    markup.add(InlineKeyboardButton("Другой", callback_data="gender_other"))
    return markup

def create_city_keyboard():
    markup = InlineKeyboardMarkup()
    # Пример городов, добавь свои
    markup.add(InlineKeyboardButton("Киров", callback_data="city_kirov"))
    return markup

def create_residential_keyboard():
    markup = InlineKeyboardMarkup()
    # Пример жилого комплекса
    markup.add(InlineKeyboardButton("Знак", callback_data="residential_znak"))
    return markup

def create_profile_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Добавить документ", callback_data="add_document"),
        InlineKeyboardButton("Добавить умение", callback_data="add_skill"),
        InlineKeyboardButton("Посмотреть заявки", callback_data="view_requests"),
        InlineKeyboardButton("В главное меню", callback_data="main_menu")
    )
    return keyboard
