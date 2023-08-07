from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.schemas import StatusMessage
from src.service import BaseService
from src.submenu.models import Submenu
from src.submenu.schemas import SubmenuCreate, SubmenuOut, SubmenuUpdate
from src.validators import validated_menu, validated_submenu

router = APIRouter(
    prefix='/menus/{menu_id}/submenus',
    tags=['Submenus'],
)


@router.post('/', response_model=SubmenuOut,
             status_code=HTTPStatus.CREATED,
             summary='Создание подменю',
             )
async def create_new_submenu(menu_id: str, submenu: SubmenuCreate,
                             session: AsyncSession = Depends(get_async_session)
                             ) -> SubmenuOut:
    service = BaseService(Submenu)
    await validated_menu.validate_id(menu_id, session)
    await validated_submenu.validate_title(submenu.title, session)
    return await service.create_subobject(menu_id, submenu, session)


@router.get('/{submenu_id}', response_model=SubmenuOut,
            status_code=HTTPStatus.OK,
            summary='Просмотр подменю по ID')
async def get_one_submenu(submenu_id: str, session: AsyncSession = Depends(get_async_session)
                          ) -> SubmenuOut:
    service = BaseService(Submenu)
    await validated_submenu.validate_id(submenu_id, session)
    return await service.get_one(submenu_id, session)


@router.get('/', response_model=list[SubmenuOut],
            status_code=HTTPStatus.OK,
            summary='Просмотр всего списка подменю по ID меню')
async def get_all_submenus(menu_id: str, session: AsyncSession = Depends(get_async_session)
                           ) -> list[SubmenuOut]:
    service = BaseService(Submenu)
    await validated_menu.validate_id(menu_id, session)
    return await service.read_all_subobjects(menu_id, session)


@router.patch('/{submenu_id}', response_model=SubmenuOut,
              status_code=HTTPStatus.OK,
              summary='Обновление подменю')
async def update_submenu(submenu_id: str, submenu_in: SubmenuUpdate,
                         session: AsyncSession = Depends(get_async_session)
                         ) -> SubmenuOut:
    service = BaseService(Submenu)
    submenu = await validated_submenu.validate_id(submenu_id, session)
    return await service.update(submenu, submenu_in, session)


@router.delete('/{submenu_id}', response_model=StatusMessage,
               status_code=HTTPStatus.OK,
               summary='Удаление подменю по ID')
async def delete_submenu(submenu_id: str,
                         session: AsyncSession = Depends(get_async_session)
                         ) -> StatusMessage:
    service = BaseService(Submenu)
    submenu = await validated_submenu.validate_id(submenu_id, session)
    submenu_name = submenu.__tablename__
    await service.delete(submenu, session)
    return StatusMessage(
        status=True,
        message=f'The {submenu_name} has been deleted',
    )
