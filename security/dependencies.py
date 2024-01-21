from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from core.security import SECRET_KEY, ALGORITHM
from db.get_db import get_db
from security.dtos.token import TokenPayload
from users.entities.users import User
from users.services.users import user_service

get_user_token = OAuth2PasswordBearer("/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_user_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return user_service.get_single_user_by_id(db, token_data.sub)


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "INACTIVE_USER"})
    return user


def get_current_supper_user(user: User = Depends(get_current_user)):
    if not user_service.is_admin():
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "Permission Denied"})
    return user


def get_api_key(request: Request):
    api_key = request.headers.get("ApiKey")
    if not api_key:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"message": "Not Authorized"})
    return str(api_key)


def get_user_by_api_key(api_key: str = Depends(get_api_key)):
    user = user_service.get_by_api_key(api_key)
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "invalid api_key"})
    return user
