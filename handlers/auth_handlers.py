from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_service
from exceptions import UserNotFoundException, UserIncorrectPasswordException
from schemas import UserLoginSchema, UserSchema
from services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/login",
    response_model=UserLoginSchema
)
async def login(
    body: UserSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:

        return auth_service.login(body.username, body.password)

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )

    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
