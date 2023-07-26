from decimal import Decimal
from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal


class DishCreate(DishBase):
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

