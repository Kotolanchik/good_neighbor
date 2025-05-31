from bot.facade import BotFacade
from bot.keyboards import create_start_keyboard, create_skills_keyboard
from bot.messages import WELCOME_TEXT, FAQ_TEXT
from telebot.types import Message, CallbackQuery
from db.database import save_user_profile, get_all_skills, add_user_skill

def register_handlers(bot):
    facade = BotFacade(bot)

    user_skills_cache = {} # временное хранилище выбранных умений {user_id: set(skill_id)}

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call: CallbackQuery):
        if call.data == 'edit_card':
            create_profile(call.message)

        elif call.data.startswith('skill_'):
            user_id = call.from_user.id
            skill_id = int(call.data.split('_')[1])

            if user_id not in user_skills_cache:
                user_skills_cache[user_id] = set()
            if skill_id in user_skills_cache[user_id]:
                user_skills_cache[user_id].remove(skill_id)
            else:
                user_skills_cache[user_id].add(skill_id)

            skills = facade.get_all_skills()
            keyboard = create_skills_keyboard(skills, user_skills_cache[user_id])
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

        elif call.data == 'skills_done':
            user_id = call.from_user.id
            selected_skills = user_skills_cache.get(user_id, set())
            # Сохраняем выбранные умения в базу
            for skill_id in selected_skills:
                add_user_skill(user_id, skill_id)
            bot.send_message(call.message.chat.id, "Умения успешно сохранены!")
            user_skills_cache.pop(user_id, None)  # очистка кеша

    def create_profile(message: Message):
        bot.send_message(message.chat.id, "Введите ваш возраст:")
        bot.register_next_step_handler(message, process_age_step)

    def process_age_step(message: Message):
        age = message.text
        bot.send_message(message.chat.id, "Укажите ваш пол (мужской/женский):")
        bot.register_next_step_handler(message, process_gender_step, age)

    def process_gender_step(message: Message, age):
        gender = message.text
        bot.send_message(message.chat.id, "Укажите ваш город:")
        bot.register_next_step_handler(message, process_city_step, age, gender)

    def process_city_step(message: Message, age, gender):
        city = message.text
        bot.send_message(message.chat.id, "Укажите ваш жилой комплекс:")
        bot.register_next_step_handler(message, process_residential_step, age, gender, city)

    def process_residential_step(message: Message, age, gender, city):
        residential = message.text
        bot.send_message(message.chat.id, "Расскажите о себе (биография):")
        bot.register_next_step_handler(message, process_bio_step, age, gender, city, residential)

    def process_bio_step(message: Message, age, gender, city, residential):
        bio = message.text
        user_data = {
            "telegram_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "age": int(age),
            "gender": gender,
            "city": city,
            "residential_complex": residential,
            "bio": bio,
            "rating": 0,
            "is_active": 1,
            "is_admin": 0
        }
        save_user_profile(user_data)

        # После сохранения профиля предлагаем выбрать умения
        skills = facade.get_all_skills()
        keyboard = create_skills_keyboard(skills)
        bot.send_message(message.chat.id, "Выберите ваши умения:", reply_markup=keyboard)
