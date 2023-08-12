from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime  # Змінили імпорт

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

# class Todo(Base):
#     __tablename__ = "todos"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(150), unique=True, index=True)
#     description: Mapped[str] = mapped_column(String(150))
#     completed: Mapped[bool] = mapped_column(default=False, nullable=True)
