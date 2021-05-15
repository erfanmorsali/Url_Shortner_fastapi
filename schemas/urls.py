from pydantic import BaseModel


class BaseUrlSchema(BaseModel):
    link: str


class UrlInDb(BaseUrlSchema):
    short_link: str = None
    owner_id: int

    class Config:
        orm_mode = True
