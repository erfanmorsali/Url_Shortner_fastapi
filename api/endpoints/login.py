from fastapi import Depends, APIRouter
from db.get_db import get_db
from services.users import user_service
from sqlalchemy.orm import Session
from schemas.users import UserInSchema, UserInDb
from fastapi import HTTPException

router = APIRouter()


@router.post("/register", response_model=UserInDb)
def register(db: Session = Depends(get_db), *, schema: UserInSchema):
    user = user_service.register(db, schema)
    return user


@router.post("/login")
def login(db: Session = Depends(get_db), *, schema: UserInSchema):
    token = user_service.authenticate(db, schema)
    if not token:
        raise HTTPException(404, detail={"message": "email or password is incorrect"})
    return {"access": token}
