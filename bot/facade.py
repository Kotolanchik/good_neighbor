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

    def save_user_to_db(self, user_data):
        """
        Сохраняет пользователя в базу данных.
        :param user_data: Словарь с данными пользователя.
        """
        session = self.db.get_session()
        try:
            user = User(
                telegram_id=user_data.get("telegram_id"),
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name")
            )
            session.add(user)
            session.commit()
            print(f"Пользователь {user_data.get('telegram_id')} сохранен в базу данных.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при сохранении пользователя: {e}")
        finally:
            session.close()

    def save_user_profile(self, user_id, profile_data):
        """
        Сохраняет или обновляет анкету пользователя.
        :param user_id: Telegram ID пользователя.
        :param profile_data: Данные анкеты.
        """
        session = self.db.get_session()
        try:
            # Проверяем, существует ли анкета пользователя
            profile = session.query(UserProfile).filter_by(user_id=user_id).first()
            if not profile:
                profile = UserProfile(user_id=user_id)
                session.add(profile)

            # Обновляем данные анкеты
            profile.age = profile_data.get("age")
            profile.gender = profile_data.get("gender")
            profile.city = profile_data.get("city")
            profile.bio = profile_data.get("bio")

            session.commit()
            print(f"Анкета пользователя {user_id} сохранена.")
        except Exception as e:
            session.rollback()
            print(f"Ошибка при сохранении анкеты: {e}")
        finally:
            session.close()
