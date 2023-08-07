from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.schemas import StatusMessage
from src.submenu.schemas import SubmenuCreate, SubmenuOut, SubmenuUpdate
from src.submenu.service import SubmenuCache, submenu_service


router = APIRouter(
    prefix='/menus/{menu_id}/submenus',
    tags=['Submenus'],
)


@router.post('/', response_model=SubmenuOut,
             status_code=HTTPStatus.CREATED,
             summary='Создание подменю',
             )
async def create_new_submenu(menu_id: str, submenu: SubmenuCreate,
                             service: SubmenuCache = Depends(submenu_service)
                             ) -> SubmenuOut:
    return await service.create_submenu(menu_id, submenu)


@router.get('/{submenu_id}', response_model=SubmenuOut,
            status_code=HTTPStatus.OK,
            summary='Просмотр подменю по ID')
async def get_one_submenu(submenu_id: str, service: SubmenuCache = Depends(submenu_service)
                          ) -> SubmenuOut:
    return await service.get_submenu(submenu_id)


@router.get('/', response_model=list[SubmenuOut],
            status_code=HTTPStatus.OK,
            summary='Просмотр всего списка подменю по ID меню')
async def get_all_submenus(menu_id: str, service: SubmenuCache = Depends(submenu_service)
                           ) -> list[SubmenuOut]:

    return await service.get_submenu_list(menu_id)


@router.patch('/{submenu_id}', response_model=SubmenuOut,
              status_code=HTTPStatus.OK,
              summary='Обновление подменю')
async def update_submenu(submenu_id: str, submenu_in: SubmenuUpdate,
                         service: SubmenuCache = Depends(submenu_service)
                         ) -> SubmenuOut:
    return await service.update_submenu(submenu_id, submenu_in)


@router.delete('/{submenu_id}', response_model=StatusMessage,
               status_code=HTTPStatus.OK,
               summary='Удаление подменю по ID')
async def delete_submenu(submenu_id: str,
                         service: SubmenuCache = Depends(submenu_service)
                         ) -> StatusMessage:
    return await service.delete_submenu(submenu_id)
