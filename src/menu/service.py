from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models import Menu
from src.menu.schemas import MenuCreate, MenuUpdate
from src.schemas import StatusMessage
from src.service import BaseService
from src.utils import clear_cache, get_cache, set_cache, CheckIdTitleExist


class MenuService:
    def __init__(self, session: AsyncSession, service: BaseService):
        self.session = session
        self.service = service
        self.check_menu = CheckIdTitleExist(Menu)

    async def create_menu(self, menu: MenuCreate):
        await self.check_menu.check_title(menu.title, self.session)
        menu = await self.service.create(menu, self.session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    async def get_menu(self, menu_id: str):
        cached = await get_cache('menu', menu_id)
        if cached:
            print('from cache')
            return cached
        await self.check_menu.check_id(menu_id, self.session)
        menu = await self.service.get_one(menu_id, self.session)
        await set_cache('menu', menu_id, menu)
        return menu

    async def get_menu_list(self):
        cached = await get_cache('menu', 'list')
        if cached:
            print('from cache')
            return cached
        menu_list = await self.service.get_many(self.session)
        await set_cache('menu', 'list', menu_list)
        return menu_list

    async def update_menu(self, menu_id: str, obj_in: MenuUpdate):
        menu = await self.check_menu.check_id(menu_id, self.session)
        menu = await self.service.update(menu, obj_in, self.session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    async def delete_menu(self, menu_id: str):
        menu = await self.check_menu.check_id(menu_id, self.session)
        await self.service.delete(menu, self.session)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The menu has been deleted',
        )


async def menu_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Menu)
    return MenuService(session=session, service=service)
