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

def create_skills_keyboard(skills, selected_skills=None):
    """
    Создаёт клавиатуру с умениями.

    :param skills: список кортежей (id, название умения)
    :param selected_skills: множество id выбранных умений (для отметки галочкой)
    :return: InlineKeyboardMarkup
    """
    if selected_skills is None:
        selected_skills = set()

    keyboard = InlineKeyboardMarkup(row_width=2)
    for skill_id, skill_name in skills:
        prefix = "✅ " if skill_id in selected_skills else ""
        button_text = f"{prefix}{skill_name}"
        keyboard.add(InlineKeyboardButton(button_text, callback_data=f"skill_{skill_id}"))

    keyboard.add(InlineKeyboardButton("Готово", callback_data="skills_done"))
    return keyboard
