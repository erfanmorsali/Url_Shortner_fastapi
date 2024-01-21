import secrets
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import create_access_token
from core.security import pwd_context
from db.get_db import get_db
from users.dtos.users import UserIn
from users.entities.users import User


class UserService:
    db: Session

    def __init__(self):
        self.db: Session = get_db()

    def get_by_id(self, pk: int) -> Type[User] | None:
        user = self.db.query(User).filter(User.id == pk).first()
        if user is None:
            raise HTTPException(404, detail={"message": "user not found"})
        return user

    def get_by_email(self, email) -> Type[User] | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_api_key(self, api_key) -> Type[User] | None:
        return self.db.query(User).filter(User.api_key == api_key).first()

    def authenticate(self, model: UserIn):
        data = model.model_dump()
        user = self.get_by_email(data.get("email"))
        if user is None or not user.is_active:
            raise HTTPException(404, detail={"message": "email or password is incorrect"})
        if self.check_password(data.get("password"), user.password):
            token = create_access_token(str(user.id))
            return token
        else:
            return None

    def register(self, model: UserIn) -> User:
        data = model.model_dump()
        user = self.get_by_email(data.get("email"))
        if user is not None:
            raise HTTPException(400, detail={"message": "user with this email already exists"})
        hashed_password = self.create_password_hash(data.get("password"))
        user_api_key = self.generate_api_key()
        del data["password"]
        data["password"] = hashed_password
        data["api_key"] = user_api_key
        user = User(**data)
        return self.commit(user)

    def commit(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    @staticmethod
    def is_admin(user: User) -> bool:
        return user.is_admin

    @staticmethod
    def check_password(password, hash_password) -> bool:
        return pwd_context.verify(password, hash_password)

    @staticmethod
    def create_password_hash(password) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def generate_api_key() -> str:
        return secrets.token_hex(25)


user_service = UserService()
