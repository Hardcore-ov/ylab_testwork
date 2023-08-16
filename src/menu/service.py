from fastapi import Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models import Menu
from src.menu.schemas import MenuCreate, MenuUpdate
from src.schemas import StatusMessage
from src.service import BaseService
from src.utils import CheckIdTitleExist
from src.utils import Cache


class MenuService:
    def __init__(self, session: AsyncSession, service: BaseService):
        self.session = session
        self.service = service
        self.check_menu = CheckIdTitleExist(Menu)
        self.cache = Cache()
        self.background_tasks: BackgroundTasks = BackgroundTasks()

    async def create_menu(self, menu: MenuCreate, menu_id: str | None = None):
        await self.check_menu.check_title(menu.title, self.session)
        menu = await self.service.create(menu, self.session, id=menu_id)
        self.background_tasks.add_task(await self.cache.set_cache('menu', menu.id, menu))
        return menu

    async def get_menu(self, menu_id: str):
        cached = await self.cache.get_cache('menu', menu_id)
        if cached:
            print('from cache')
            return cached
        await self.check_menu.check_id(menu_id, self.session)
        menu = await self.service.get_one(menu_id, self.session)
        self.background_tasks.add_task(await self.cache.set_cache('menu', menu_id, menu))
        return menu

    async def get_menu_list(self):
        cached = await self.cache.get_cache('menu', 'list')
        if cached:
            print('from cache')
            return cached
        menu_list = await self.service.get_many(self.session)
        self.background_tasks.add_task(await self.cache.set_cache('menu', 'list', menu_list))
        return menu_list

    async def get_all_menu(self):
        return await self.service.read_all_menu(self.session)

    async def update_menu(self, menu_id: str, obj_in: MenuUpdate):
        menu = await self.check_menu.check_id(menu_id, self.session)
        menu = await self.service.update(menu, obj_in, self.session)
        self.background_tasks.add_task(await self.cache.set_cache('menu', menu.id, menu))
        self.background_tasks.add_task(await self.cache.clear_cache('menu', 'list'))
        return menu

    async def delete_menu(self, menu_id: str):
        menu = await self.check_menu.check_id(menu_id, self.session)
        await self.service.delete(menu, self.session)
        self.background_tasks.add_task(await self.cache.clear_cache('menu', menu_id))
        self.background_tasks.add_task(await self.cache.clear_cache('menu', 'list'))
        return StatusMessage(
            status=True,
            message='The menu has been deleted',
        )

    async def update_data_from_file(self, menu_data: dict) -> None:
        all_menu_id = await self.session.execute(select(Menu.id))
        await self.session.commit()
        for menu_id in all_menu_id.all():
            menu_id = menu_id[0]
            if menu_id in menu_data:
                await self.update_menu(menu_id, MenuUpdate(**menu_data[menu_id]))

                menu_data.pop(menu_id)
            else:
                await self.delete_menu(menu_id)
        for menu_id, data in menu_data.items():
            await self.create_menu(MenuCreate(**data), menu_id=menu_id)


async def menu_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Menu)
    return MenuService(session=session, service=service)
