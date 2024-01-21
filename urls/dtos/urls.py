from pydantic import BaseModel


class BaseUrlDto(BaseModel):
    link: str


class UrlOut(BaseUrlDto):
    short_link: str = None
    owner_id: int

    class Config:
        orm_mode = True
