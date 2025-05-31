import sqlite3

conn = sqlite3.connect('db.sqlite', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    username TEXT,
    first_name TEXT,
    age INTEGER,
    gender TEXT,
    city TEXT,
    residential_complex TEXT,
    bio TEXT,
    rating INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    is_admin INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    skill_id INTEGER,
    level TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_path TEXT NOT NULL,
    doc_type TEXT,
    description TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')


def init_skills():
    skills_list = [
        ("Первая помощь", "Навыки оказания экстренной помощи при травмах и несчастных случаях"),
        ("Починка техники", "Ремонт мелкой бытовой техники и электроники"),
        ("Выгуливание собак", "Ответственный выгул и уход за домашними животными"),
        ("Помощь по дому", "Уборка, мелкий ремонт, помощь пожилым и занятым соседям"),
        ("Уход за детьми", "Присмотр, игры и помощь в уходе за детьми"),
        ("Покупка и доставка продуктов", "Помощь с покупками и доставкой продуктов и необходимых товаров"),
        ("Садоводство", "Уход за растениями, цветами и огородом"),
        ("Мелкий ремонт", "Починка мебели, сантехники и электроприборов"),
        ("Общение и поддержка", "Психологическая поддержка и приятное общение с соседями"),
        ("Доставка лекарств", "Покупка и доставка лекарств по рецептам и назначению")
    ]
    for name, desc in skills_list:
        add_skill(name, desc)


conn.commit()
init_skills()


# Функция сохранения/обновления профиля пользователя
def save_user_profile(user_data):
    cursor.execute('''
        INSERT OR REPLACE INTO users 
        (telegram_id, username, first_name, age, gender, city, residential_complex, bio, rating, is_active, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_data['telegram_id'],
        user_data.get('username'),
        user_data.get('first_name'),
        user_data.get('age'),
        user_data.get('gender'),
        user_data.get('city'),
        user_data.get('residential_complex'),
        user_data.get('bio'),
        user_data.get('rating', 0),
        user_data.get('is_active', 1),
        user_data.get('is_admin', 0)
    ))
    conn.commit()

# Получить ID пользователя по telegram_id
def get_user_id(telegram_id):
    cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
    result = cursor.fetchone()
    return result[0] if result else None

# Добавить новый скилл (если ещё нет)
def add_skill(name, description=None):
    try:
        cursor.execute('INSERT INTO skills (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # скилл с таким именем уже есть

# Получить все скиллы
def get_all_skills():
    cursor.execute('SELECT id, name, description FROM skills')
    return cursor.fetchall()

# Добавить скилл пользователю с уровнем
def add_user_skill(telegram_id, skill_name, level):
    user_id = get_user_id(telegram_id)
    if not user_id:
        return False
    cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
    skill = cursor.fetchone()
    if not skill:
        add_skill(skill_name)
        cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
        skill = cursor.fetchone()
    skill_id = skill[0]
    # Проверим, есть ли уже этот скилл у пользователя
    cursor.execute('SELECT id FROM user_skills WHERE user_id = ? AND skill_id = ?', (user_id, skill_id))
    exists = cursor.fetchone()
    if exists:
        cursor.execute('UPDATE user_skills SET level = ? WHERE id = ?', (level, exists[0]))
    else:
        cursor.execute('INSERT INTO user_skills (user_id, skill_id, level) VALUES (?, ?, ?)', (user_id, skill_id, level))
    conn.commit()
    return True

# Получить скиллы пользователя
def get_user_skills(telegram_id):
    user_id = get_user_id(telegram_id)
    if not user_id:
        return []
    cursor.execute('''
        SELECT skills.name, user_skills.level 
        FROM user_skills 
        JOIN skills ON user_skills.skill_id = skills.id
        WHERE user_skills.user_id = ?
    ''', (user_id,))
    return cursor.fetchall()

# Добавить документ пользователя
def add_document(telegram_id, file_path, doc_type=None, description=None):
    user_id = get_user_id(telegram_id)
    if not user_id:
        return False
    cursor.execute('''
        INSERT INTO documents (user_id, file_path, doc_type, description) 
        VALUES (?, ?, ?, ?)
    ''', (user_id, file_path, doc_type, description))
    conn.commit()
    return True

# Получить документы пользователя
def get_user_documents(telegram_id):
    user_id = get_user_id(telegram_id)
    if not user_id:
        return []
    cursor.execute('''
        SELECT file_path, doc_type, description, uploaded_at 
        FROM documents 
        WHERE user_id = ?
    ''', (user_id,))
    return cursor.fetchall()



