import uuid

from fastapi_users import schemas
from fastapi_users.models import ID


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: ID
    username: str
    role_id: ID


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: ID


class UserUpdate(schemas.BaseUserUpdate):
    pass