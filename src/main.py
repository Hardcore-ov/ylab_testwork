from fastapi import FastAPI

from src.router import main_router

app = FastAPI(title='Menu app')

app.include_router(main_router)
