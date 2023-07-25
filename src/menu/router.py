from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.menu.schemas import MenuCreate, MenuOut, MenuUpdate
from src.menu.models import Menu
from src.service import BaseService
from src.schemas import StatusMessage
from src.validators import validated_menu
from src.database import get_async_session

router = APIRouter(
    prefix="/menus",
    tags=["Menus"],
)


@router.post(
    "/",
    response_model=MenuOut,
    status_code=HTTPStatus.CREATED,
    summary="Создание меню",
)
async def create_new_menu(
    menu: MenuCreate, session: AsyncSession = Depends(get_async_session)
 ) -> MenuOut:
    service = BaseService(Menu)
    return await service.create(obj_in=menu, session=session)


@router.get("/{menu_id}", response_model=MenuOut,
                          status_code=HTTPStatus.OK,
                          summary="Просмотр меню по id",
)
async def get_one_menu(menu_id: str, session: AsyncSession = Depends(get_async_session)) -> MenuOut:
    return await validated_menu.validate_id(menu_id, session)


@router.get("/", response_model=list[MenuOut],
                 status_code=HTTPStatus.OK,
                 summary="Просмотр всего списка меню",
)
async def get_all_menus(session: AsyncSession = Depends(get_async_session)) -> list[MenuOut]:
    service = BaseService(Menu)
    return await service.get_many(session)


@router.patch("/{menu_id}", response_model=MenuOut,
                            status_code=HTTPStatus.OK,
                            summary="Обновление меню",
)
async def to_update_menu(menu_id: str, menu_in: MenuUpdate, session: AsyncSession = Depends(get_async_session)) -> MenuOut:
    service = BaseService(Menu)
    menu = await validated_menu.validate_id(menu_id, session)
    return await service.update(menu, menu_in, session)


@router.delete('/{menu_id}', response_model=StatusMessage,
                             status_code=HTTPStatus.OK,
                             summary="Удаление меню по id",
)
async def delete_menu(menu_id: str, db: Session = Depends(get_async_session)) -> StatusMessage:
    menu = await validated_menu.validate_id(menu_id, db)
    await db.delete(menu)
    await db.commit()
    return StatusMessage(
        status=True,
        message="The menu has been deleted",
    )


