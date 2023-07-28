"""Модуль содержит бизнес логику работы приложения"""
from uuid import UUID

from fastapi import status, HTTPException

from app.api import repositories, schemas
from app.utils import funcs


class Services:
    """
    Класс содержит обработчики для роутов

    Methods:
        create(self, create_data: schemas.CreateRequest)
        get(self, uuid: UUID)
        select_all_with_paginate(self, page: int, page_size: int)
        select_all_with_count(self, counter: int)
        delete(self, uuid: UUID)

    """

    def __init__(self, storage: repositories.RepositoryWorker):
        self._storage = storage

    async def create(self, create_data: schemas.CreateRequest) -> schemas.CreateResponse:
        """
        Метод для создания новой записи

        Args:
            create_data: Данные для создания записи

        Returns:
            созданная запись

        """
        response = await self._storage.insert(create_data=create_data)
        response_schema = schemas.CreateResponse(uuid=str(response.uuid), text=response.text)
        return response_schema

    async def get(self, uuid: UUID) -> schemas.GetResponse:
        """
        Метод для получения записи по UUID

        Args:
            uuid: идентификатор записи

        Returns:
            запись

        Raises:
            HTTPException: если запись не найдена

        """
        response = await self._storage.select_by_uuid(uuid=uuid)
        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

        response_schema = schemas.GetResponse(uuid=str(response.uuid), text=response.text)
        return response_schema

    async def select_all_with_paginate(self, page: int, page_size: int) -> schemas.GetAllResponse:
        """
        Метод для получения пагинированного списка записей

        Args:
            page: номер страницы
            page_size: размер страницы

        Returns:
            список записей

        Raises:
            HTTPException: если количество записей <= 0 или отрицательное

        """
        if page <= 0 or page_size <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="page or page-size can't be 0 or less than 0")

        response = await self._storage.select_all_with_paginate(page=page, page_size=page_size)
        list_messages = list(map(lambda x: schemas.GetResponse(uuid=str(x.uuid), text=x.text), response))
        total_rows_count = await self._storage.get_rows_count()
        all_pages = funcs.get_all_pages(total_rows_count=total_rows_count, page_size=page_size)
        response_schema = schemas.GetAllResponse(page=page, all_pages=all_pages,
                                                 page_size=page_size, messages=list_messages,
                                                 total_count=total_rows_count, data_on_page=len(response))

        return response_schema

    async def select_all_with_count(self, counter: int) -> list[schemas.GetResponse]:
        """
        Метод для получения списка записей в виде списка определённой длины

        Args:
            counter: количество записей

        Returns:
            список записей

        Raises:
            HTTPException: если количество записей <= 0 или отрицательное

        """
        if counter <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="count can't be 0 or less than 0")

        response = await self._storage.select_all_with_count(counter=counter)
        response_schema = list(map(lambda x: schemas.GetResponse(uuid=str(x.uuid), text=x.text), response))
        return response_schema

    async def delete(self, uuid: UUID) -> None:
        """
        Метод для удаления записи

        Args:
            uuid: идентификатор записи

        Raises:
            HTTPException: если запись не найдена

        """
        if not await self._storage.select_by_uuid(uuid=uuid):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

        await self._storage.delete_by_id(uuid=uuid)
