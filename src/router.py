from fastapi import APIRouter

from src.menu.router import router

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(router)
