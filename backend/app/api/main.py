from fastapi import APIRouter

from .routes import users, items, login


api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(items.router, prefix='/items', tags=['items'])
