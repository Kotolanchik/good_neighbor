# db/models.py

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    Модель для хранения пользователей Telegram.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

class UserProfile(Base):
    """
    Модель для хранения анкеты пользователя.
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)  # Связь с таблицей users через telegram_id
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    city = Column(String(255), nullable=True)
    bio = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, age={self.age}, gender={self.gender})>"