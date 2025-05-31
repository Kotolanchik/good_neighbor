from bot.facade import BotFacade
from bot.keyboards import (
    create_start_keyboard,
    create_skills_keyboard,
    create_gender_keyboard,
    create_city_keyboard,
    create_residential_keyboard,
    create_profile_inline_keyboard,
)
from bot.messages import WELCOME_TEXT
from telebot.types import Message, CallbackQuery

def register_handlers(bot, conn):
    facade = BotFacade(bot, conn)
    user_skills_cache = {}
    user_temp_data = {}

    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=create_start_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data == 'edit_card')
    def edit_card_handler(call: CallbackQuery):
        create_profile(call.message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('skill_'))
    def skill_toggle_handler(call: CallbackQuery):
        telegram_id = call.from_user.id
        skill_id = int(call.data.split('_')[1])

        if telegram_id not in user_skills_cache:
            user_skills_cache[telegram_id] = set()

        if skill_id in user_skills_cache[telegram_id]:
            user_skills_cache[telegram_id].remove(skill_id)
        else:
            user_skills_cache[telegram_id].add(skill_id)

        skills = facade.get_all_skills()
        keyboard = create_skills_keyboard(skills, user_skills_cache[telegram_id])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data == 'skills_done')
    def save_skills(call: CallbackQuery):
        telegram_id = call.from_user.id
        selected_skills = user_skills_cache.get(telegram_id, set())

        # Можно добавить метод для очистки текущих умений, если надо
        # facade.clear_user_skills(telegram_id)

        for skill_id in selected_skills:
            facade.add_user_skill(telegram_id, skill_id)
        user_skills_cache.pop(telegram_id, None)

        bot.answer_callback_query(call.id)
        text = format_user_profile(telegram_id)
        markup = create_profile_inline_keyboard()
        bot.send_message(call.message.chat.id, "Умения успешно сохранены!")
        bot.send_message(call.message.chat.id, text, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("gender_"))
    def handle_gender(call: CallbackQuery):
        gender = call.data.split("_")[1]
        telegram_id = call.from_user.id

        if telegram_id not in user_temp_data:
            user_temp_data[telegram_id] = {}

        user_temp_data[telegram_id]["gender"] = gender

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Выберите ваш город:", reply_markup=create_city_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data.startswith("city_"))
    def handle_city(call: CallbackQuery):
        city = call.data.split("_")[1]
        telegram_id = call.from_user.id

        if telegram_id not in user_temp_data:
            user_temp_data[telegram_id] = {}

        user_temp_data[telegram_id]["city"] = city

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Выберите жилой комплекс:", reply_markup=create_residential_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data.startswith("residential_"))
    def handle_residential(call: CallbackQuery):
        residential = call.data.split("_")[1]
        telegram_id = call.from_user.id

        if telegram_id not in user_temp_data:
            user_temp_data[telegram_id] = {}

        user_temp_data[telegram_id]["residential_complex"] = residential

        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Расскажите о себе (биография):")
        bot.register_next_step_handler(call.message, process_bio_step, telegram_id)

    def create_profile(message: Message):
        bot.send_message(message.chat.id, "Введите ваш возраст:")
        bot.register_next_step_handler(message, process_age_step)

    def process_age_step(message: Message):
        age = message.text
        telegram_id = message.from_user.id
        if telegram_id not in user_temp_data:
            user_temp_data[telegram_id] = {}
        user_temp_data[telegram_id]["age"] = age
        bot.send_message(message.chat.id, "Укажите ваш пол:", reply_markup=create_gender_keyboard())

    def process_bio_step(message: Message, telegram_id):
        bio = message.text

        temp = user_temp_data.get(telegram_id, {})
        user_data = {
            "telegram_id": telegram_id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "age": int(temp.get("age", 18)),
            "gender": temp.get("gender", "не указан"),
            "city": temp.get("city", "не указан"),
            "residential_complex": temp.get("residential_complex", "не указан"),
            "bio": bio,
            "rating": 0,
            "is_active": 1,
            "is_admin": 0
        }
        facade.save_user_profile(user_data)

        skills = facade.get_all_skills()
        keyboard = create_skills_keyboard(skills)
        bot.send_message(message.chat.id, "Выберите ваши умения:", reply_markup=keyboard)

    def format_user_profile(telegram_id):
        user_data = facade.get_user_profile(telegram_id)
        user_skills = facade.get_user_skills(telegram_id)

        if not user_data:
            return "Профиль не найден."

        skills_text = ', '.join(user_skills) if user_skills else "не указаны"

        text = (
            f"Ваш профиль:\n"
            f"Возраст: {user_data.get('age', 'не указан')}\n"
            f"Пол: {user_data.get('gender', 'не указан')}\n"
            f"Город: {user_data.get('city', 'не указан')}\n"
            f"Жилой комплекс: {user_data.get('residential_complex', 'не указан')}\n"
            f"Биография: {user_data.get('bio', 'не указана')}\n"
            f"Умения: {skills_text}"
        )
        return text
