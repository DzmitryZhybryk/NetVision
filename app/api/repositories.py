"""Модуль содержит репозитории для взаимодействия с внешними хранилищами данных"""
from typing import Sequence
from uuid import UUID

import sqlalchemy
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import interfaces, schemas
from app.database import models
from app.utils import decorators


class MessagesRepository(interfaces.BaseRepositoryInterface):
    """Класс реализует интерфейсы родительского класса взаимодействия с внешними хранилищами данных"""

    def __init__(self, session: AsyncSession) -> None:
        """Метод инициализации объектов репозитория"""
        super().__init__(session)
        self._session = session
        self._schema = models.Message

    async def select_by_id(self, uuid: UUID) -> models.Message:
        """Метод реализует логику родительского класса взаимодействия с внешними хранилищами данных"""
        stmt = sqlalchemy.select(models.Message).where(models.Message.uuid == uuid)
        database_response = await self._session.scalar(stmt)
        return database_response

    async def get_rows_count(self) -> int:
        """Метод реализует логику родительского класса взаимодействия с внешними хранилищами данных"""
        stmt = sqlalchemy.select(sqlalchemy.func.count(models.Message.uuid))
        database_response = await self._session.execute(stmt)
        count = database_response.scalar_one()
        return count

    async def select_all_with_paginate(self, page: int, page_size: int) -> Sequence[Row | RowMapping]:
        """Метод реализует логику родительского класса взаимодействия с внешними хранилищами данных"""
        stmt = sqlalchemy.select(models.Message).offset((page - 1) * page_size).limit(page_size)
        database_response = await self._session.execute(stmt)
        result = database_response.scalars().all()
        return result

    async def select_all_with_count(self, counter: int) -> Sequence[Row | RowMapping]:
        """Метод реализует логику родительского класса взаимодействия с внешними хранилищами данных"""
        stmt = sqlalchemy.select(models.Message).limit(counter)
        database_response = await self._session.execute(stmt)
        result = database_response.scalars().all()
        return result

    @decorators.integrity_error_handler
    async def insert(self, create_data: schemas.CreateRequest) -> models.Message:
        """Метод реализует логику родительского класса взаимодействия с внешними хранилищами данных"""
        stmt = sqlalchemy.insert(models.Message).returning(models.Message).values(**create_data.model_dump())
        database_response = await self._session.execute(stmt)
        new_message = database_response.scalar_one()
        await self._session.commit()
        return new_message

    async def delete_by_id(self, uuid: UUID) -> None:
        """Метод реализует логику родительского класса взаимодействия с внешними хранилищами данных"""
        stmt = sqlalchemy.delete(models.Message).where(models.Message.uuid == uuid)
        await self._session.execute(stmt)
        await self._session.commit()


class RepositoryWorker:

    def __init__(self, main_database: interfaces.BaseRepositoryInterface):
        self._main_database = main_database

    async def select_by_uuid(self, uuid: UUID) -> models.Message:
        """
        Метод получает запись из базы данных по UUID

        Args:
            uuid: идентификатор записи в базе данных

        Returns:
            запись из базы данных

        """
        response = await self._main_database.select_by_id(uuid=uuid)
        return response

    async def select_all_with_paginate(self, page: int, page_size: int) -> Sequence:
        """
        Метод получает записи из базы данных для последующей пагинации

        Args:
            page: номер страницы
            page_size: размер страницы

        Returns:
            список записей из базы данных

        """
        response = await self._main_database.select_all_with_paginate(page=page, page_size=page_size)
        return response

    async def get_rows_count(self) -> int:
        """
        Метод получает количество записей в базе данных

        Returns:
            количество записей

        """
        response = await self._main_database.get_rows_count()
        return response

    async def insert(self, create_data: schemas.CreateRequest) -> models.Message:
        """
        Метод создает запись в базе данных

        Args:
            create_data: данные для создания записи

        Returns:
            созданная запись

        """
        response = await self._main_database.insert(create_data=create_data)
        return response

    async def select_all_with_count(self, counter: int) -> Sequence:
        """
        Метод получает записи из базы данных в виде списка определённой длины

        Args:
            counter: количество записей в базе данных, которые надо вернуть

        Returns:
            список записей из базы данных

        """
        response = await self._main_database.select_all_with_count(counter=counter)
        return response

    async def delete_by_id(self, uuid: UUID) -> None:
        """
        Метод удаляет запись из базы данных

        Args:
            uuid: идентификатор записи в базе данных

        """
        await self._main_database.delete_by_id(uuid=uuid)
