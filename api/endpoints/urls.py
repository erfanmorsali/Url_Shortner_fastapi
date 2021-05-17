from fastapi import APIRouter, Depends
from models.urls import Url
from services.urls import url_service
from schemas.urls import BaseUrlSchema, UrlInDb
from typing import List
from sqlalchemy.orm import Session
from db.get_db import get_db
from api.deps import get_current_user , get_user_by_api_key
from models.users import User
from fastapi import HTTPException


router = APIRouter()


@router.post("/create_url", response_model=UrlInDb, status_code=201)
def create_url(db: Session = Depends(get_db), *, input_data: BaseUrlSchema,
               current_user: User = Depends(get_user_by_api_key)):
    url = url_service.create_url(db, input_data, current_user)
    return url


@router.get("/urls", response_model=List[UrlInDb])
def all_urls(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    urls = url_service.get_all_urls(db)
    return urls


@router.get("/{short_link}" , response_model=UrlInDb)
def get_url(short_link : str , db: Session = Depends(get_db)):
    url = url_service.get_url_by_short_link(db,short_link)
    return url


@router.get("/{url_id}")
def get_single_url(url_id: int, db: Session = Depends(get_db)):
    return db.query(Url).filter(Url.id == url_id).first()


@router.delete("/{short_link}",status_code=204)
def remove_ur_by_short_linkl(short_link : str , db : Session = Depends(get_db),current_user : User = Depends(get_user_by_api_key)):
    url = url_service.get_url_by_short_link(db,short_link)
    if url.owner_id == current_user.id:
        url_service.remove_url(url,db)
    else:
        raise HTTPException(403, detail={"message": "Foebiden"})

@router.put("/update_url/{url_id}", response_model=UrlInDb)
def update_url(url_id: int, input_data: BaseUrlSchema, db: Session = Depends(get_db)):
    return url_service.update_url(db, url_id, input_data)


