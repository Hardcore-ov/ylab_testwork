from http import HTTPStatus

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.dish.models import Dish
from src.dish.service import DishService
from src.menu.models import Menu
from src.menu.service import MenuService
from src.schemas import StatusMessage
from src.service import BaseService
from src.submenu.models import Submenu
from src.submenu.service import SubmenuService
from src.tasks.utils import get_data_from_excel_file, is_change
from src.tasks.worker import app

task_router = APIRouter(
    prefix='/update_from_file',
    tags=['Updates']
)


@task_router.get('', status_code=HTTPStatus.ACCEPTED,
                 summary='Проверка изменения файла Excel')
async def excel_to_db(session: AsyncSession = Depends(get_async_session)):
    return await check_and_update_excel_file(session)


@task_router.get('/manual', status_code=HTTPStatus.CREATED,
                 summary='Внести данные из Excel-файла в БД')
async def excel_to_db_manual(session: AsyncSession = Depends(get_async_session)):
    new_data = get_data_from_excel_file()
    return await update_data(new_data, session)


async def check_and_update_excel_file(session: AsyncSession):
    if is_change():
        new_data = get_data_from_excel_file()
        await update_data(new_data, session)
        if new_data is False:
            return StatusMessage(
                status=False,
                message='Discount field must be an integer number!',
            )
        else:
            return {'result': 'Begin to update!'}
    return {'result': 'No data to change'}


async def update_menu(menu_data: dict,
                      session: AsyncSession):
    service = BaseService(Menu)
    menu_service = MenuService(session, service)
    await menu_service.update_data_from_file(menu_data)


async def update_submenu(submenu_data: dict,
                         session: AsyncSession):
    service = BaseService(Submenu)
    submenu_service = SubmenuService(session, service)
    await submenu_service.update_data_from_file(submenu_data)


async def update_dish(dish_data: dict,
                      session: AsyncSession):
    service = BaseService(Dish)
    dish_service = DishService(session, service)
    await dish_service.update_data_from_file(dish_data)


async def update_data(excel_data: tuple,
                      session: AsyncSession = Depends(get_async_session)):
    if excel_data is False:
        return StatusMessage(
            status=False,
            message='Discount field must be an integer number!',
        )
    menu_data, submenu_data, dish_data = excel_data
    await update_menu(menu_data, session)
    await update_submenu(submenu_data, session)
    await update_dish(dish_data, session)
    return {'result': 'Database data updated successfully!'}


app.conf.beat_schedule = {
    'check-and-update-every-15-seconds': {
        'task': 'src.tasks.tasks.check_and_update_excel_file_task',
        'schedule': 15.0,
    },
}

app.conf.update(task_track_started=True)


@app.task
def check_and_update_excel_file_task():
    session = requests.Session()
    request = session.get('http://web:8000/api/v1/update_from_file')
    return request.text


if __name__ == '__main__':
    beat = app.Beat(loglevel='debug')
    beat.start_scheduler()
