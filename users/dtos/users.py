from pydantic import BaseModel


class BaseUserDto(BaseModel):
    email: str


class UserIn(BaseUserDto):
    password: str


class UserOut(BaseUserDto):
    id: int

    class Config:
        orm_mode = True
