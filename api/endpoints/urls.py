from fastapi import APIRouter, Depends
from models.urls import Url
from services.urls import url_service
from schemas.urls import BaseUrlSchema, UrlInDb
from typing import List
from sqlalchemy.orm import Session
from db.get_db import get_db
from api.deps import get_current_user
from models.users import User

router = APIRouter()


@router.post("/create_url", response_model=UrlInDb, status_code=201)
def create_url(db: Session = Depends(get_db), *, input_data: BaseUrlSchema,
               current_user: User = Depends(get_current_user)):
    url = url_service.create_url(db, input_data, current_user)
    return url


@router.get("/urls", response_model=List[UrlInDb])
def all_urls(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    urls = url_service.get_all_urls(db)
    return urls


@router.get("/{url_id}")
def get_single_url(url_id: int, db: Session = Depends(get_db)):
    return db.query(Url).filter(Url.id == url_id).first()


@router.put("/update_url/{url_id}", response_model=UrlInDb)
def update_url(url_id: int, input_data: BaseUrlSchema, db: Session = Depends(get_db)):
    return url_service.update_url(db, url_id, input_data)
