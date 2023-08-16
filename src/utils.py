import json
import uuid
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import redis


def generate_uuid():
    return str(uuid.uuid4())


class Cache:

    def generate_key(self, prefix, body):
        key = f'{prefix}:{body}'
        return key

    async def get_cache(self, prefix, body):
        key = self.generate_key(prefix, body)
        value = await redis.get(key)
        return json.loads(value) if value else None

    async def set_cache(self, prefix, body, value):
        key = self.generate_key(prefix, body)
        await redis.set(key, json.dumps(jsonable_encoder(value)))

    async def clear_cache(self, prefix, body):
        key = self.generate_key(prefix, body)
        keys = await redis.keys(f'{key}*')
        if keys:
            await redis.delete(*keys)


class CheckIdTitleExist:
    def __init__(self, model):
        self.model = model

    async def check_id(self, check_id: str, session: AsyncSession):
        model_name = self.model.__tablename__
        query = select(self.model).where(self.model.id == check_id)
        check_object = await session.execute(query)
        check_object = check_object.scalars().first()
        if check_object is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'{model_name} not found')
        return check_object

    async def check_title(self, check_title: str, session: AsyncSession) -> None:
        model_name = self.model.__tablename__
        check_obj = await session.execute(
            select(self.model.id).where(
                self.model.title == check_title))
        check_title = check_obj.scalars().first()
        if check_title is not None:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f'{model_name} с таким именем уже существует!',
            )
        return check_title
