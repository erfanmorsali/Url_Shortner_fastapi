from passlib.context import CryptContext
from typing import Union, Any
from datetime import timedelta, datetime
from jose import jwt
import secrets

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=120
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
