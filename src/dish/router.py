from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dish.schemas import DishCreate, DishOut, DishUpdate
from src.dish.models import Dish
from src.service import BaseService
from src.schemas import StatusMessage
from src.validators import validated_dish, validated_submenu
from src.database import get_async_session

router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
)


@router.post("/", response_model=DishOut,
                  status_code=HTTPStatus.CREATED,
                  summary="Создание блюда",
)
async def create_new_dish(submenu_id: str, dish: DishCreate,
                          session: AsyncSession = Depends(get_async_session)
                          ) -> DishOut:
    service = BaseService(Dish)
    await validated_submenu.validate_id(submenu_id, session)
    await validated_dish.validate_title(dish.title, session)
    return await service.create_dish(submenu_id, dish, session)


@router.get("/{dish_id}", response_model=DishOut,
                          status_code=HTTPStatus.OK,
                          summary="Просмотр блюда по ID")
async def get_one_dish(dish_id: str, session: AsyncSession = Depends(get_async_session)
                       ) -> DishOut:
    service = BaseService(Dish)
    await validated_dish.validate_id(dish_id, session)
    return await service.get_one(dish_id, session)


@router.get("/", response_model=list[DishOut],
                 status_code=HTTPStatus.OK,
                 summary="Просмотр всего списка блюд")
async def get_all_dishes(session: AsyncSession = Depends(get_async_session)
                        ) -> list[DishOut]:
    service = BaseService(Dish)
    return await service.get_many(session)


@router.patch("/{dish_id}", response_model=DishOut,
                            status_code=HTTPStatus.OK,
                            summary="Обновление блюда")
async def update_dish(dish_id: str, dish_in: DishUpdate,
                      session: AsyncSession = Depends(get_async_session)
                      ) -> DishOut:
    service = BaseService(Dish)
    dish = await validated_dish.validate_id(dish_id, session)
    return await service.update(dish, dish_in, session)


@router.delete('/{dish_id}', response_model=StatusMessage,
                             status_code=HTTPStatus.OK,
                             summary="Удаление блюда по ID")
async def delete_dish(dish_id: str,
                      session: AsyncSession = Depends(get_async_session)
                      ) -> StatusMessage:
    service = BaseService(Dish)
    dish = await validated_dish.validate_id(dish_id, session)
    dish_name = dish.__tablename__
    await service.delete(dish, session)
    return StatusMessage(
        status=True,
        message=f"The {dish_name} has been deleted",
    )


