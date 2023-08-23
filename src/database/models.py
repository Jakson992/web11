from datetime import date

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func  # Змінили імпорт
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.database.db import Base

from pydantic import BaseModel


class SearchContactParams(BaseModel):
    name: str


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)  # Виправили тут
    first_name = Column(String, index=True)  # Виправили тут
    last_name = Column(String, index=True)  # Виправили тут
    email = Column(String, unique=True, index=True)  # Виправили тут
    phone_number = Column(String)  # Виправили тут
    birthday = Column(DateTime)  # Виправили тут
    additional_info = Column(String, nullable=True)  # Виправили тут
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship('User', backref="todos", lazy='joined')


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    avatar: Mapped[str] = Column(String(255), nullable=True)
    refresh_token: Mapped[str] = Column(String(255), nullable=True)

# class Todo(Base):
#     __tablename__ = "todos"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(150), unique=True, index=True)
#     description: Mapped[str] = mapped_column(String(150))
#     completed: Mapped[bool] = mapped_column(default=False, nullable=True)
