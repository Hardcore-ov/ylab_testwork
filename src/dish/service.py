from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.validators import validated_dish, validated_submenu
from src.utils import clear_cache, get_cache, set_cache
from src.database import get_async_session
from src.schemas import StatusMessage
from src.dish.models import Dish
from src.service import BaseService


class DishCache:
    def __init__(self, session, service):
        self.session = session
        self.service = service

    async def create_dish(self, submenu_id, dish):
        await validated_submenu.validate_id(submenu_id, self.session)
        await validated_dish.validate_title(dish.title, self.session)
        dish = await self.service.create_dish(submenu_id, dish, self.session)
        await set_cache('dish', dish.id, dish)
        await clear_cache(submenu_id, 'dish')
        await clear_cache('submenu', submenu_id)
        await clear_cache('menu', 'list')
        return dish

    async def get_dish_list(self, submenu_id):
        cached = await get_cache(submenu_id, 'dish')
        if cached:
            print('from cache')
            return cached
        dish_list = await self.service.read_all_dishes(submenu_id, self.session)
        await set_cache(submenu_id, 'dish', dish_list)
        return dish_list

    async def get_dish(self, dish_id):
        cached = await get_cache('dish', dish_id)
        if cached:
            print('from cache')
            return cached
        await validated_dish.validate_id(dish_id, self.session)
        dish = await self.service.get_one(dish_id, self.session)
        await set_cache('dish', dish_id, dish)
        return dish

    async def update_dish(self, dish_id, obj_in):
        dish = await validated_dish.validate_id(dish_id, self.session)
        dish = await self.service.update(dish, obj_in, self.session)
        await set_cache('dish', dish_id, dish)
        await clear_cache(dish.submenu_id, 'dish')
        await clear_cache('submenu', dish.submenu_id)
        await clear_cache('menu', 'list')
        return dish

    async def delete_dish(self, dish_id):
        dish = await validated_dish.validate_id(dish_id, self.session)
        await self.service.delete(dish, self.session)
        await clear_cache('dish', dish_id)
        await clear_cache(dish.submenu_id, 'dish')
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The dish has been deleted',
        )


async def dish_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Dish)
    return DishCache(session=session, service=service)
