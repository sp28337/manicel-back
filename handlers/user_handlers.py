from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_user_service, get_request_user_id
from exceptions import UserNameAlreadyExistsException, UserEmailAlreadyExistsException, UserIncorrectPasswordException
from schemas import UserCreateSchema, UserLoginSchema, UserProfileSchema
from services import UserService


router = APIRouter(prefix="/user", tags=["user"])


@router.get(path="/profile/{user_id}", response_model=UserProfileSchema)
async def read_user_profile(
    user_id: Annotated[int, Depends(get_request_user_id)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    return user_service.read_user_profile(user_id=user_id)


@router.post(path="", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        return user_service.create_user(
            username=body.username,
            password=body.password,
            email=body.email
        )

    except (UserNameAlreadyExistsException, UserEmailAlreadyExistsException) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )


@router.patch(path="/update_username/{user_id}", response_model=UserProfileSchema)
async def update_username(
        user_id: Annotated[int, Depends(get_request_user_id)],
        new_username: str,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    try:
        return user_service.update_username(user_id=user_id, new_username=new_username)

    except UserNameAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail
        )


@router.patch(path="/update_name/{user_id}", response_model=UserProfileSchema)
async def update_name(
        user_id: Annotated[int, Depends(get_request_user_id)],
        new_name: str,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    return user_service.update_name(user_id=user_id, new_name=new_name)


@router.patch(path="/update_password/{user_id}", response_model=UserProfileSchema)
async def update_password(
        user_id: Annotated[int, Depends(get_request_user_id)],
        new_password: str,
        user_service: Annotated[UserService, Depends(get_user_service)],
        old_password: str | None = None,
):
    try:
        return user_service.update_password(
            user_id=user_id,
            old_password=old_password,
            new_password=new_password
        )

    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
