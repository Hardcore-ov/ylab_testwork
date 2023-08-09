from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.dish.schemas import DishCreate, DishOut, DishUpdate
from src.dish.service import DishService, dish_service
from src.schemas import StatusMessage

router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dishes'],
)


@router.post('/', response_model=DishOut,
             status_code=HTTPStatus.CREATED,
             summary='Создание блюда',
             )
async def create_new_dish(submenu_id: str, dish: DishCreate,
                          service: DishService = Depends(dish_service)
                          ) -> DishOut:
    return await service.create_dish(submenu_id, dish)


@router.get('/{dish_id}', response_model=DishOut,
            status_code=HTTPStatus.OK,
            summary='Просмотр блюда по ID')
async def get_one_dish(dish_id: str, service: DishService = Depends(dish_service)
                       ) -> DishOut:
    return await service.get_dish(dish_id)


@router.get('/', response_model=list[DishOut],
            status_code=HTTPStatus.OK,
            summary='Просмотр всего списка блюд по ID подменю')
async def get_all_dishes(submenu_id: str,
                         service: DishService = Depends(dish_service)
                         ) -> list[DishOut]:
    return await service.get_dish_list(submenu_id)


@router.patch('/{dish_id}', response_model=DishOut,
              status_code=HTTPStatus.OK,
              summary='Обновление блюда')
async def update_dish(dish_id: str, dish_in: DishUpdate,
                      service: DishService = Depends(dish_service)
                      ) -> DishOut:
    return await service.update_dish(dish_id, dish_in)


@router.delete('/{dish_id}', response_model=StatusMessage,
               status_code=HTTPStatus.OK,
               summary='Удаление блюда по ID')
async def delete_dish(dish_id: str,
                      service: DishService = Depends(dish_service)
                      ) -> StatusMessage:
    return await service.delete_dish(dish_id)
