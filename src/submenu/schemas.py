from typing import ClassVar

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My submenu 1",
                "description": "My submenu description 1",
            },
        }


class SubmenuUpdate(SubmenuBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My updated submenu 1",
                "description": "My updated submenu description 1",
            },
        }


class SubmenuOut(SubmenuBase):
    id: str
    dishes_count: int

    class Config:
        from_attributes = True

