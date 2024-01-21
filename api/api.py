from fastapi import APIRouter

from security.controllers import login
from urls.controllers import urls
from users.controllers import users

api_router = APIRouter()
api_router.include_router(urls.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
