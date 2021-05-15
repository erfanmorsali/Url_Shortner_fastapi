import pdb

from models.users import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.users import UserInSchema
from core.security import pwd_context
from core.security import create_access_token
import secrets


class UserService:
    def get_single_user_by_id(self, db: Session, pk: int):
        user = db.query(User).filter(User.id == pk).first()
        if user is None:
            raise HTTPException(404, detail={"message": "user not found"})
        return user

    def get_user_by_email(self, db: Session, email):
        user = db.query(User).filter(User.email == email).first()
        return user

    def get_user_by_api_key(self, db: Session, api_key):
        user = db.query(User).filter(User.api_key == api_key).first()
        return user

    def get_user_urls(self, db: Session, user_id):
        user = db.query(User).filter(User.id == user_id).one()
        return user

    def authenticate(self, db: Session, schema: UserInSchema):
        data = schema.dict()
        user = self.get_user_by_email(db, data.get("email"))
        if user is None or not user.is_active:
            raise HTTPException(404, detail={"message": "email or password is incorrect"})
        if self.check_user_password(data.get("password"), user.password):
            token = create_access_token(str(user.id))
            return token
        else:
            return None

    def generate_api_key(self):
        return secrets.token_hex(25)

    def register(self, db: Session, schema: UserInSchema):
        data = schema.dict()
        user = self.get_user_by_email(db, data.get("email"))
        if user is not None:
            raise HTTPException(400, detail={"message": "user with this email already exists"})
        hashed_password = self.create_password_hash(data.get("password"))
        user_api_key = self.generate_api_key()
        del data["password"]
        data["password"] = hashed_password
        data["api_key"] = user_api_key
        user = User(**data)
        return self.commit_user_to_database(user, db)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.is_admin

    def commit_user_to_database(self, user: User, db: Session):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def check_user_password(self, password, hash_password):
        return pwd_context.verify(password, hash_password)

    def create_password_hash(self, password):
        return pwd_context.hash(password)


user_service = UserService()
