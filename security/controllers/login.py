from fastapi import APIRouter
from fastapi import HTTPException

from users.dtos.users import UserIn, UserOut
from users.services.users import user_service

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserOut)
def register(*, model: UserIn):
    return user_service.register(model)


@router.post("/login")
def login(*, model: UserIn):
    token = user_service.authenticate(model)
    if not token:
        raise HTTPException(404, detail={"message": "email or password is incorrect"})
    return {"access": token}
