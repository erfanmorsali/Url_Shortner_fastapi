from pydantic import BaseModel
from schemas.urls import UrlInDb
from typing import List


class BaseUserSchema(BaseModel):
    email: str


class UserInSchema(BaseUserSchema):
    password: str


class UserInDb(BaseUserSchema):
    password: str

    class Config:
        orm_mode = True


class UserUrls(BaseModel):
    urls: List[UrlInDb]

    class Config:
        orm_mode = True
