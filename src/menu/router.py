from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.menu.schemas import MenuCreate, MenuOut, MenuUpdate, MenuAll
from src.menu.service import MenuService, menu_service
from src.schemas import StatusMessage

router = APIRouter(
    prefix='/menus',
    tags=['Menus'],
)


@router.post('/', response_model=MenuOut,
             status_code=HTTPStatus.CREATED,
             summary='Создание меню')
async def create_new_menu(menu: MenuCreate,
                          service: MenuService = Depends(menu_service)
                          ) -> MenuOut:
    return await service.create_menu(menu)


@router.get('/{menu_id}', response_model=MenuOut,
            status_code=HTTPStatus.OK,
            summary='Просмотр меню по ID')
async def get_one_menu(menu_id: str,
                       service: MenuService = Depends(menu_service)
                       ) -> MenuOut:
    return await service.get_menu(menu_id)


@router.get('/', response_model=list[MenuOut],
            status_code=HTTPStatus.OK,
            summary='Просмотр всего списка меню')
async def get_all_menus(service: MenuService = Depends(menu_service)
                        ) -> list[MenuOut]:
    return await service.get_menu_list()


@router.patch('/{menu_id}', response_model=MenuOut,
              status_code=HTTPStatus.OK,
              summary='Обновление меню')
async def update_menu(menu_id: str, menu_in: MenuUpdate,
                      service: MenuService = Depends(menu_service)
                      ) -> MenuOut:
    return await service.update_menu(menu_id, menu_in)


@router.delete('/{menu_id}', response_model=StatusMessage,
               status_code=HTTPStatus.OK,
               summary='Удаление меню по ID')
async def delete_menu(menu_id: str,
                      service: MenuService = Depends(menu_service)
                      ) -> StatusMessage:
    return await service.delete_menu(menu_id)


@router.get('/all/', response_model=list[MenuAll],
            status_code=HTTPStatus.OK,
            summary='Просмотр всего дерева меню, подменю, блюд')
async def get_all_menus(service: MenuService = Depends(menu_service)) -> list[MenuAll]:
    return await service.get_all_menu()
