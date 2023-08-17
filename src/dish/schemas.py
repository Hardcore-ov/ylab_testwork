from decimal import Decimal

from pydantic import validator

from src.schemas import SchemaBase


class DishBase(SchemaBase):

    price: Decimal
    discount: int

    @validator('price')
    def check_price(cls, value: Decimal):
        return format(float(value), '.2f')


class DishCreate(DishBase):

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '12.50',
                'discount': '0',
            },
        }


class DishUpdate(DishBase):
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '14.50',
                'discount': '10'
            },
        }


class DishOut(DishBase):
    id: str

    class Config:
        from_attributes = True
