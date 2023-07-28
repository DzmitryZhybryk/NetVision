"""Модуль содержит модели базы данных"""

import sqlalchemy
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base


class Message(Base):
    """Модель базы данных, описывающая сущность Message"""
    __tablename__ = "messages"

    uuid: Mapped[UUID] = mapped_column(sqlalchemy.UUID, primary_key=True, unique=True)
    text: Mapped[str] = mapped_column(sqlalchemy.Text, nullable=False)

    def __str__(self) -> str:
        return f"User(id={self.uuid!r}, username={self.text!r})"

    def __repr__(self) -> str:
        return str(self)

    def dict(self) -> dict:
        return self.__dict__
