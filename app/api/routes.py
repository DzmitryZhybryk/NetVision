"""Модуль содержит роуты предоставляющие внешний API"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api import services, schemas, responses, dependencies

router = APIRouter()
BaseHandlerDep = Annotated[services.Services, Depends(dependencies.services_worker)]


@router.post("/messages/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.CreateResponse,
             responses=responses.create_responses)
async def create(create_data: schemas.CreateRequest, handler: BaseHandlerDep):
    response = await handler.create(create_data=create_data)
    return response


@router.get("/messages/{uuid}/",
            response_model=schemas.GetResponse,
            responses=responses.get_responses)
async def get(uuid: UUID, handler: BaseHandlerDep):
    response = await handler.get(uuid=uuid)
    return response


@router.get("/messages/",
            response_model=schemas.GetAllResponse,
            responses=responses.get_all_response)
async def get_all_with_paginate(page: int, page_size: int, handler: BaseHandlerDep):
    response = await handler.select_all_with_paginate(page=page, page_size=page_size)
    return response


@router.get("/messages/{counter}/count/")
async def get_all_with_count(counter: int, handler: BaseHandlerDep):
    response = await handler.select_all_with_count(counter=counter)
    return response


@router.delete("/messages/{uuid}/",
               status_code=status.HTTP_204_NO_CONTENT,
               responses=responses.delete_response)
async def delete(uuid: UUID, handler: BaseHandlerDep):
    await handler.delete(uuid=uuid)
