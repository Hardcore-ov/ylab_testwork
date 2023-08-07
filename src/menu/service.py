from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models import Menu
from src.utils import clear_cache, get_cache, set_cache
from src.schemas import StatusMessage
from src.service import BaseService
from src.validators import validated_menu


class MenuCache:
    def __init__(self, session, service):
        self.session = session
        self.service = service

    async def create_menu(self, menu):
        await validated_menu.validate_title(menu.title, self.session)
        menu = await self.service.create(menu, self.session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    async def get_menu(self, menu_id):
        cached = await get_cache('menu', menu_id)
        if cached:
            print('from cache')
            return cached
        await validated_menu.validate_id(menu_id, self.session)
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

    async def update_menu(self, menu_id, obj_in):
        menu = await validated_menu.validate_id(menu_id, self.session)
        menu = await self.service.update(menu, obj_in, self.session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    async def delete_menu(self, menu_id):
        menu = await validated_menu.validate_id(menu_id, self.session)
        await self.service.delete(menu, self.session)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The menu has been deleted',
        )


async def menu_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Menu)
    return MenuCache(session=session, service=service)
