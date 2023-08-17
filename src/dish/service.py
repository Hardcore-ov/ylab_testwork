from fastapi import BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.dish.models import Dish
from src.dish.schemas import DishCreate, DishUpdate
from src.schemas import StatusMessage
from src.service import BaseService
from src.submenu.models import Submenu
from src.utils import Cache, CheckIdTitleExist, discount


class DishService:
    def __init__(self, session: AsyncSession, service: BaseService):
        self.session = session
        self.service = service
        self.check_dish = CheckIdTitleExist(Dish)
        self.check_submenu = CheckIdTitleExist(Submenu)
        self.cache = Cache()
        self.background_tasks: BackgroundTasks = BackgroundTasks()

    async def create_dish(self, submenu_id: str, dish: DishCreate, dish_id: str | None = None):
        await self.check_submenu.check_id(submenu_id, self.session)
        await self.check_dish.check_title(dish.title, self.session)
        dish = await self.service.create_dish(submenu_id, dish, self.session, id=dish_id)
        self.background_tasks.add_task(await self.cache.set_cache('dish', dish.id, dish))
        self.background_tasks.add_task(await self.cache.clear_cache(submenu_id, 'dish'))
        self.background_tasks.add_task(await self.cache.clear_cache('submenu', submenu_id))
        self.background_tasks.add_task(await self.cache.clear_cache('menu', 'list'))
        return dish

    async def get_dish_list(self, submenu_id: str):
        cached = await self.cache.get_cache(submenu_id, 'dish')
        if cached:
            for index, cache in enumerate(cached):
                cached[index]['price'] = discount(cache['price'], cache['discount'])
            print('from cache')
            return cached
        dish_list = await self.service.read_all_dishes(submenu_id, self.session)
        for index, dish in enumerate(dish_list):
            dish = jsonable_encoder(dish)
            dish['price'] = discount(dish['price'], dish['discount'])
            dish_list[index] = dish
        self.background_tasks.add_task(await self.cache.set_cache(submenu_id, 'dish', dish_list))
        return dish_list

    async def get_dish(self, dish_id: str):
        cached = await self.cache.get_cache('dish', dish_id)
        if cached:
            cached['price'] = discount(cached['price'], cached['discount'])
            print('from cache')
            return cached
        await self.check_dish.check_id(dish_id, self.session)
        dish = await self.service.get_one(dish_id, self.session)
        if dish is not None:
            dish = jsonable_encoder(dish)
            dish['price'] = discount(dish['price'], dish['discount'])
        self.background_tasks.add_task(await self.cache.set_cache('dish', dish_id, dish))
        return dish

    async def update_dish(self, dish_id: str, obj_in: DishUpdate):
        dish = await self.check_dish.check_id(dish_id, self.session)
        dish = await self.service.update(dish, obj_in, self.session)
        self.background_tasks.add_task(await self.cache.set_cache('dish', dish_id, dish))
        self.background_tasks.add_task(await self.cache.clear_cache(dish.submenu_id, 'dish'))
        self.background_tasks.add_task(await self.cache.clear_cache('submenu', dish.submenu_id))
        self.background_tasks.add_task(await self.cache.clear_cache('menu', 'list'))
        return dish

    async def delete_dish(self, dish_id: str):
        dish = await self.check_dish.check_id(dish_id, self.session)
        await self.service.delete(dish, self.session)
        self.background_tasks.add_task(await self.cache.clear_cache('dish', dish_id))
        self.background_tasks.add_task(await self.cache.clear_cache(dish.submenu_id, 'dish'))
        self.background_tasks.add_task(await self.cache.clear_cache('menu', 'list'))
        return StatusMessage(
            status=True,
            message='The dish has been deleted',
        )

    async def update_data_from_file(self, dish_data: dict) -> None:
        all_dish_id = await self.session.execute(select(Dish.id))
        await self.session.commit()
        all_dish_id = all_dish_id.all()
        for dish_id in all_dish_id:
            dish_id = dish_id[0]
            if dish_id in dish_data:
                data = dish_data[dish_id]
                data.pop('submenu_id')
                await self.update_dish(dish_id, DishUpdate(**data))
                dish_data.pop(dish_id)
            else:
                await self.delete_dish(dish_id)
        for dish_id, data in dish_data.items():
            submenu_id = data.pop('submenu_id')
            await self.create_dish(submenu_id, DishCreate(**data), dish_id)


async def dish_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Dish)
    return DishService(session=session, service=service)
