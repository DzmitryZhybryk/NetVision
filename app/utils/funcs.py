"""Модуль содержит вспомогательный функции"""

import math

from app.utils import decorators


@decorators.handle_zero_division_error
def get_all_pages(total_rows_count: int, page_size: int) -> int:
    """
    Метод возвращает количество страниц при разбиении всех пользователей на страницы.

    Args:
        total_rows_count: Количество записей в базе данных
        page_size: Размер страницы

    Returns:
        Количество страниц.

    """
    return math.ceil(total_rows_count / page_size) or 1
