"""Модуль содержит интерфейс работы с внешним хранилищем данных"""
from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.api import schemas


class BaseRepositoryInterface(ABC):
    """
    Класс интерфейс работы с внешним хранилищем данных

    Methods:
        select_by_id(self, uuid: UUID)
        select_all_with_paginate(self, page: int, page_size: int)
        insert(self, create_data: schemas.CreateRequest)
        delete_by_id(self, uuid: UUID)
        get_rows_count(self)
        select_all_with_count(self, counter: int)

    """

    def __init__(self, session: object) -> None:
        self.session = session

    @abstractmethod
    async def select_by_id(self, uuid: UUID):
        """
        Метод для получения данных из хранилища

        Args:
            uuid: Уникальный идентификатор записи

        Returns:
            Полученную запись

        """
        pass

    @abstractmethod
    async def select_all_with_paginate(self, page: int, page_size: int) -> Sequence:
        """
        Метод для получения данных из хранилища в виде списка с фильтрами для пагинации

        Args:
            page: Номер страницы
            page_size: Размер страницы

        Returns:
            Список записей

        """
        pass

    @abstractmethod
    async def insert(self, create_data: schemas.CreateRequest):
        """
        Метод для добавления данных в хранилище

        Args:
            create_data: Данные для добавления

        Returns:
            Добавленная запись

        """
        pass

    @abstractmethod
    async def delete_by_id(self, uuid: UUID) -> None:
        """
        Метод для удаления данных из хранилища

        Args:
            uuid: Уникальный идентификатор записи

        """
        pass

    @abstractmethod
    async def get_rows_count(self) -> int:
        """Метод для получения количества записей в хранилище"""
        pass

    @abstractmethod
    async def select_all_with_count(self, counter: int) -> Sequence:
        """
        Метод для получения данных из хранилища в виде списка определенной длины

        Args:
            counter: Количество записей, которые будут возвращены

        """
        pass
