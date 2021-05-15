from fastapi import APIRouter, Depends
from api.deps import get_user_by_api_key, get_db
from services.users import user_service
from schemas.users import UserUrls
from models.users import User
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/users/user_all_urls", response_model=UserUrls)
def get_user_urls(db: Session = Depends(get_db), user: User = Depends(get_user_by_api_key)):
    urls = user_service.get_user_urls(db, user.id)
    return urls
