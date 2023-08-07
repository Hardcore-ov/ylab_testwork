from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dish.models import Dish
from src.menu.models import Menu
from src.submenu.models import Submenu


class Validation:
    def __init__(self, model):
        self.model = model

    async def validate_id(self, validation_id: str,
                          session: AsyncSession):
        model_name = self.model.__tablename__
        query = select(self.model).where(self.model.id == validation_id)
        validation_object = await session.execute(query)
        validation_object = validation_object.scalars().first()
        if validation_object is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'{model_name} not found',
            )
        return validation_object

    async def validate_title(self, validation_title: str,
                             session: AsyncSession) -> None:
        model_name = self.model.__tablename__
        validation_obj = await session.execute(
            select(self.model.id).where(
                self.model.title == validation_title,
            ),
        )
        validation_title = validation_obj.scalars().first()
        if validation_title is not None:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f'{model_name} с таким именем уже существует!',
            )
        return validation_title


validated_menu = Validation(Menu)
validated_submenu = Validation(Submenu)
validated_dish = Validation(Dish)
