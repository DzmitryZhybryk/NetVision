"""Модуль содержит декораторы"""
from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def integrity_error_handler(func):
    """
    Декоратор, принимает функцию и обрабатывает исключение integrity error от Postgres

    Args:
        func: функция, которая может вызвать ошибку integrity error

    Returns:
        обработанная функция

    Raises:
        HTTPException: если было отловлено исключение integrity error

    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="The same data already exist in database")

    return wrapper


def handle_zero_division_error(func):
    """
    Декоратор для обработки ошибки ZeroDivisionError.

    Args:
        func: функция, которая может вызвать ошибку ZeroDivisionError.

    Returns:
        обработанная функция

    Raises:
        HTTPException: если производится деление на 0

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError as ex:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail={"message": "Zero division error",
                                        "exception": f"{ex}"})

    return wrapper
