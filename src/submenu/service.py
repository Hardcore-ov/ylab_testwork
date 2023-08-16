from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models import Menu
from src.schemas import StatusMessage
from src.service import BaseService
from src.submenu.models import Submenu
from src.submenu.schemas import SubmenuCreate, SubmenuUpdate
from src.utils import CheckIdTitleExist, clear_cache, get_cache, set_cache


class SubmenuService:
    def __init__(self, session: AsyncSession, service: BaseService):
        self.session = session
        self.service = service
        self.check_menu = CheckIdTitleExist(Menu)
        self.check_submenu = CheckIdTitleExist(Submenu)

    async def create_submenu(self, menu_id: str, submenu: SubmenuCreate, submenu_id: str | None = None):
        await self.check_menu.check_id(menu_id, self.session)
        await self.check_submenu.check_title(submenu.title, self.session)
        submenu = await self.service.create_subobject(menu_id, submenu, self.session, id=submenu_id)
        await set_cache('submenu', submenu.id, submenu)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return submenu

    async def get_submenu_list(self, menu_id: str):
        await self.check_menu.check_id(menu_id, self.session)
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
        await self.check_submenu.check_id(submenu_id, self.session)
        submenu = await self.service.get_one(submenu_id, self.session)
        await set_cache('submenu', submenu_id, submenu)
        return submenu

    async def update_submenu(self, submenu_id: str, obj_in: SubmenuUpdate):
        submenu = await self.check_submenu.check_id(submenu_id, self.session)
        submenu = await self.service.update(submenu, obj_in, self.session)
        await set_cache('submenu', submenu_id, submenu)
        await clear_cache(submenu.menu_id, 'submenu')
        await clear_cache('menu', submenu.menu_id)
        await clear_cache('menu', 'list')
        return submenu

    async def delete_submenu(self, submenu_id: str):
        submenu = await self.check_submenu.check_id(submenu_id, self.session)
        await self.service.delete(submenu, self.session)
        await clear_cache('submenu', submenu_id)
        await clear_cache(submenu.menu_id, 'submenu')
        await clear_cache('menu', submenu.menu_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The submenu has been deleted',
        )

    async def update_data_from_file(self, submenu_data: dict) -> None:
        all_menu_id = await self.session.execute(select(Submenu.id))
        await self.session.commit()
        for submenu_id in all_menu_id.all():
            submenu_id = str(submenu_id[0])
            if submenu_id in submenu_data:
                data = submenu_data[submenu_id]
                data.pop('menu_id')
                await self.update_submenu(submenu_id, SubmenuUpdate(**data))
                submenu_data.pop(submenu_id)
            else:
                await self.delete_submenu(submenu_id)
        for submenu_id, data in submenu_data.items():
            menu_id = data.pop('menu_id')
            await self.create_submenu(menu_id, SubmenuCreate(**data), submenu_id)


async def submenu_service(session: AsyncSession = Depends(get_async_session)):
    service = BaseService(Submenu)
    return SubmenuService(session=session, service=service)
