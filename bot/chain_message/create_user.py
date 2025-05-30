@bot.message_handler(commands=["edit_card"])
def create_profile(message: Message):
    """
    Команда /create_profile.
    """
    bot.send_message(message.chat.id, "Введите ваш возраст:")
    bot.register_next_step_handler(message, process_age_step)

def process_age_step(message: Message):
    """
    Обработка шага ввода возраста.
    """
    age = message.text
    bot.send_message(message.chat.id, "Укажите ваш пол (мужской/женский):")
    bot.register_next_step_handler(message, process_gender_step, age)

def process_gender_step(message: Message, age):
    """
    Обработка шага ввода пола.
    """
    gender = message.text
    bot.send_message(message.chat.id, "Укажите ваш город:")
    bot.register_next_step_handler(message, process_city_step, age, gender)

def process_city_step(message: Message, age, gender):
    """
    Обработка шага ввода города.
    """
    city = message.text
    bot.send_message(message.chat.id, "Расскажите о себе (биография):")
    bot.register_next_step_handler(message, process_bio_step, age, gender, city)

def process_bio_step(message: Message, age, gender, city):
    """
    Обработка шага ввода биографии.
    """
    bio = message.text
    profile_data = {
        "age": int(age),
        "gender": gender,
        "city": city,
        "bio": bio
    }
    facade.save_user_profile(message.from_user.id, profile_data)
    bot.send_message(message.chat.id, "Ваша анкета успешно создана!")