from src.schemas import SchemaBase


class MenuCreate(SchemaBase):
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'My menu 1',
                'description': 'My menu description 1',
            },
        }


class MenuUpdate(SchemaBase):
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'My updated menu 1',
                'description': 'My updated menu description 1',
            },
        }


class MenuOut(SchemaBase):
    id: str
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True
