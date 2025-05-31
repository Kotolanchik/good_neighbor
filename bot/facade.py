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

    def save_user_profile(self, profile_data):
        self.cursor.execute('''
                INSERT OR REPLACE INTO users 
                (telegram_id, username, first_name, age, gender, city, residential_complex, bio, rating, is_active, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            profile_data['telegram_id'],
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
        user_id = self.get_user_id_by_telegram_id(telegram_id)
        if user_id is None:
            return
        self.cursor.execute('''
            INSERT OR IGNORE INTO user_skills (user_id, skill_id) VALUES (?, ?)
        ''', (user_id, skill_id))
        self.conn.commit()

    def get_user_skills(self, telegram_id):
        user_id = self.get_user_id_by_telegram_id(telegram_id)
        if not user_id:
            return []
        self.cursor.execute('''
            SELECT s.name FROM skills s
            JOIN user_skills us ON s.id = us.skill_id
            WHERE us.user_id = ?
        ''', (user_id,))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_user_profile(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        row = self.cursor.fetchone()
        if row is None:
            return None

        columns = [desc[0] for desc in self.cursor.description]
        user_data = dict(zip(columns, row))


        gender_map = {
            "male": "Мужской",
            "female": "Женский",
            None: "не указан"
        }
        city_map = {
            "kirov": "Киров",
            "moscow": "Москва",
            "spb": "Санкт-Петербург",
            None: "не указан"
        }
        residential_map = {
            "znak": "Знак",
            None: "не указан"
        }

        # Перевод значений, если есть в словарях, иначе оставить как есть или "не указан"
        user_data['gender'] = gender_map.get(user_data.get('gender'), user_data.get('gender', 'не указан'))
        user_data['city'] = city_map.get(user_data.get('city'), user_data.get('city', 'не указан'))
        user_data['residential_complex'] = residential_map.get(user_data.get('residential_complex'),
                                                               user_data.get('residential_complex', 'не указан'))

        return user_data

    def get_user_id_by_telegram_id(self, telegram_id):
        self.cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

