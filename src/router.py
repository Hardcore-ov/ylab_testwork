from fastapi import APIRouter

from src.dish.router import router as dish_router
from src.menu.router import router as menu_router
from src.submenu.router import router as submenu_router
from src.tasks.tasks import task_router

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(menu_router)
main_router.include_router(submenu_router)
main_router.include_router(dish_router)
main_router.include_router(task_router)
