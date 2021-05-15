from fastapi import APIRouter
from api.endpoints import urls, users, login

api_router = APIRouter()
api_router.include_router(urls.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
