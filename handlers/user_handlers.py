from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_user_service
from exceptions import UserNameAlreadyExistsException, UserEmailAlreadyExistsException
from schemas import UserCreateSchema, UserLoginSchema
from services import UserService


router = APIRouter(prefix="/user", tags=["user"])


@router.post(path="", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        return user_service.create_user(username=body.username, password=body.password, email=body.email)

    except (UserNameAlreadyExistsException, UserEmailAlreadyExistsException) as e:
        raise HTTPException(
            status_code=403,
            detail=e.detail
        )
