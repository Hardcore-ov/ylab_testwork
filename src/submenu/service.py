from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.schemas import StatusMessage
from src.service import BaseService
from src.submenu.models import Submenu
from src.submenu.schemas import SubmenuCreate, SubmenuUpdate
from src.utils import clear_cache, get_cache, set_cache
from src.validators import validated_menu, validated_submenu


class SubmenuService:
    def __init__(self, session: AsyncSession, service: BaseService):
        self.session = session
        self.service = service

    async def create_submenu(self, menu_id: str, submenu: SubmenuCreate):
        await validated_menu.validate_id(menu_id, self.session)
        await validated_submenu.validate_title(submenu.title, self.session)
        submenu = await self.service.create_subobject(
            menu_id,
            submenu,
            self.session,
        )
        await set_cache('submenu', submenu.id, submenu)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return submenu

    async def get_submenu_list(self, menu_id: str):
        await validated_menu.validate_id(menu_id, self.session)
        cached = await get_cache(menu_id, 'submenu')
        if cached:
            print('from cache')
            return cached
        submenu_list = await self.service.read_all_subobjects(menu_id, self.session)
        await set_cache(menu_id, 'submenu', submenu_list)
        return submenu_list

    async def get_submenu(self, submenu_id: str):
        cached = await get_cache('submenu', submenu_id)
        if cached:
            print('from cache')
            return cached
        await validated_submenu.validate_id(submenu_id, self.session)
        submenu = await self.service.get_one(submenu_id, self.session)
        await set_cache('submenu', submenu_id, submenu)
        return submenu

    async def update_submenu(self, submenu_id: str, obj_in: SubmenuUpdate):
        submenu = await validated_submenu.validate_id(submenu_id, self.session)
        submenu = await self.service.update(submenu, obj_in, self.session)
        await set_cache('submenu', submenu_id, submenu)
        await clear_cache(submenu.menu_id, 'submenu')
        await clear_cache('menu', submenu.menu_id)
        await clear_cache('menu', 'list')
        return submenu

    async def delete_submenu(self, submenu_id: str):
        submenu = await validated_submenu.validate_id(submenu_id, self.session)
        await self.service.delete(submenu, self.session)
        await clear_cache('submenu', submenu_id)
        await clear_cache(submenu.menu_id, 'submenu')
        await clear_cache('menu', submenu.menu_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The submenu has been deleted',
        )


async def submenu_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Submenu)
    return SubmenuService(session=session, service=service)
