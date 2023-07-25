import decimal

from pydantic import BaseModel
from sqlalchemy import Numeric


class DishBase(BaseModel):
    title: str
    description: str
    price: float

class DishCreate(DishBase):
    submenu_id = str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My dish 1",
                "description": "My dish description 1",
                "price": "12.50",
            },
        }


class DishUpdate(DishCreate):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My updated dish 1",
                "description": "My updated dish description 1",
                "price": "14.50",
            },
        }


class DishOut(DishBase):
    id: str

    class Config:
        from_attributes = True

