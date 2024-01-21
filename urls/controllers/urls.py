from typing import List

from fastapi import APIRouter, Depends

from security.dependencies import get_user_by_api_key
from urls.dtos.urls import BaseUrlDto, UrlOut
from urls.services.urls import url_service
from users.entities.users import User

router = APIRouter(prefix="/urls")


@router.post("", response_model=UrlOut, status_code=201)
def create(*, input_data: BaseUrlDto, current_user: User = Depends(get_user_by_api_key)):
    return url_service.create(input_data, current_user)


@router.get("", response_model=List[UrlOut])
def get_all():
    return url_service.get_all()


@router.get("/{id}")
def get_by_id(id: int):
    return url_service.get_by_id(id)


@router.get("/search/{short_link}", response_model=UrlOut)
def get_by_short_link(short_link: str):
    url = url_service.get_by_short_link(short_link)
    return url


@router.delete("/{short_link}", status_code=204)
def remove_by_short_link(short_link: str):
    url = url_service.get_by_short_link(short_link)
    url_service.delete(url)


@router.put("/{id}", response_model=UrlOut)
def update_url(id: int, input_data: BaseUrlDto):
    return url_service.update(id, input_data)
