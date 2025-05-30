# db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def create_engine(self):
        """Создает соединение с базой данных."""
        try:
            db_url = (
                f"postgresql+psycopg2://"
                f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
                f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            )
            engine = create_engine(db_url)
            print("Успешное подключение к базе данных!")
            return engine
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def get_session(self):
        """Возвращает новую сессию для работы с базой данных."""
        return self.Session()