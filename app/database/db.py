"""Модуль содержит соединения с базой данных"""
from typing import AsyncGenerator

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import config

engine = create_async_engine(config.database_url, echo=config.postgres_echo)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def use_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция создает сессию базы данных

    Returns:
        сессию базы данных

    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
