from src.dish.schemas import DishOut
from src.schemas import SchemaBase


class SubmenuCreate(SchemaBase):
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'My submenu 1',
                'description': 'My submenu description 1',
            },
        }


class SubmenuUpdate(SchemaBase):
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'My updated submenu 1',
                'description': 'My updated submenu description 1',
            },
        }


class SubmenuOut(SchemaBase):
    id: str
    dishes_count: int

    class Config:
        from_attributes = True


class SubmenuAll(SchemaBase):
    id: str
    dishes: list[DishOut] | None = None

    class Config:
        from_attributes = True
