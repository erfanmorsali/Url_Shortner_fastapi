from typing import List

from fastapi import APIRouter, Depends

from security.dependencies import get_user_by_api_key
from urls.dtos.urls import UrlOut
from urls.services.urls import url_service
from users.entities.users import User

router = APIRouter(prefix="/users")


@router.get("/urls", response_model=List[UrlOut])
def get_user_urls(current_user: User = Depends(get_user_by_api_key)):
    return url_service.get_by_owner_id(current_user.id)
