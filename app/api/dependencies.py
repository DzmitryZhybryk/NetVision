"""Модуль для хранения зависимостей приложения"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import repositories, services, interfaces
from app.database.db import use_session


def database_storage(session: AsyncSession = Depends(use_session)) -> interfaces.BaseRepositoryInterface:
    """Зависимость, принимает сессию базы данных и возвращает экземпляр класса репозитория"""
    return repositories.MessagesRepository(session=session)


def repository_worker(main_database=Depends(database_storage)) -> repositories.RepositoryWorker:
    """Зависимость, принимает репозиторий с сессией базы данных и возвращает интерфейс работы с ним"""
    return repositories.RepositoryWorker(main_database=main_database)


def services_worker(storage=Depends(repository_worker)) -> services.Services:
    """
    Зависимость, принимает интерфейс для работы с репозиторием базы данных и возвращает класс, содержащий бизнес логику
    """
    return services.Services(storage=storage)
