from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class BotFacade:
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn
        self.cursor = conn.cursor()

    def send_inline_keyboard(self, chat_id, text, buttons):
        keyboard = InlineKeyboardMarkup(row_width=1)
        for text_btn, callback in buttons:
            keyboard.add(InlineKeyboardButton(text_btn, callback_data=callback))
        self.bot.send_message(chat_id, text, reply_markup=keyboard)

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id, text)

    def get_all_skills(self):
        self.cursor.execute("SELECT id, name FROM skills ORDER BY id")
        return self.cursor.fetchall()

    def save_user_profile(self, telegram_id, profile_data):
        # пример сохранения данных пользователя
        # тут надо добавить корректную логику вставки/обновления в таблицу users
        self.cursor.execute('''
            INSERT INTO users (telegram_id, username, first_name, age, gender, city, residential_complex, bio, rating, is_active, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                age=excluded.age,
                gender=excluded.gender,
                city=excluded.city,
                residential_complex=excluded.residential_complex,
                bio=excluded.bio
        ''', (
            telegram_id,
            profile_data.get('username'),
            profile_data.get('first_name'),
            profile_data.get('age'),
            profile_data.get('gender'),
            profile_data.get('city'),
            profile_data.get('residential_complex'),
            profile_data.get('bio'),
            profile_data.get('rating', 0),
            profile_data.get('is_active', 1),
            profile_data.get('is_admin', 0)
        ))
        self.conn.commit()

    def add_user_skill(self, telegram_id, skill_id):
        # Добавить умение для пользователя (в таблицу user_skills)
        self.cursor.execute('''
            INSERT OR IGNORE INTO user_skills (user_telegram_id, skill_id) VALUES (?, ?)
        ''', (telegram_id, skill_id))
        self.conn.commit()
