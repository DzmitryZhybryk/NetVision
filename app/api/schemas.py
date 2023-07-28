"""Модуль содержит pydantic схемы для валидации данных"""
from uuid import UUID, uuid4

from pydantic import BaseModel


class GetResponse(BaseModel):
    uuid: str
    text: str

    class Config:
        json_schema_extra = {
            'example': {
                'uuid': str(uuid4()),
                'text': 'some text'
            }
        }


class BasePaginator(BaseModel):
    page: int
    page_size: int
    all_pages: int
    total_count: int
    data_on_page: int


class GetAllResponse(BasePaginator):
    messages: list[GetResponse]

    class Config:
        json_schema_extra = {
            'example': {
                'current_page': '1',
                'all_pages': '20',
                'page_size': '20',
                'total_count': '12',
                'data_on_page': '20',
                'messages': [
                    {
                        'uuid': str(uuid4()),
                        'text': 'some text'
                    }
                ],
            }
        }


class CreateRequest(BaseModel):
    uuid: UUID
    text: str


class CreateResponse(GetResponse):
    pass


class UpdateRequest(BaseModel):
    pass


class UpdateResponse(BaseModel):
    pass

    class Config:
        json_schema_extra = {
            'example': {
                'some': 'data',
            }
        }
