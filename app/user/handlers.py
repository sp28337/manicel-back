from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.exceptions import (
    UserNameAlreadyExistsException,
    UserEmailAlreadyExistsException,
    UserIncorrectPasswordException,
    UserNotFoundException,
)
from app.user.schemas import (
    UserCreateSchema,
    UserProfileSchema,
    UserUpdatePasswordSchema,
    ReadUserProfileSchema,
    UserUpdateNameSchema,
    UserUpdateEmailSchema,
    UserUpdateUsernameSchema,
)
from app.dependencies import get_user_service, get_request_user_id
from app.user.auth.schemas import UserLoginSchema
from app.user.service import UserService


router = APIRouter(prefix="/user", tags=["user"])


@router.get(path="/profile/{user_id}", response_model=ReadUserProfileSchema)
async def read_user_profile(
    user_id: Annotated[int, Depends(get_request_user_id)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.read_user_profile(user_id=user_id)


@router.post(path="", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_service.create_user(
            username=body.username, password=body.password, email=body.email
        )

    except (UserNameAlreadyExistsException, UserEmailAlreadyExistsException) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.patch(path="/update_username/{user_id}", response_model=UserProfileSchema)
async def update_username(
    user_id: Annotated[int, Depends(get_request_user_id)],
    body: UserUpdateUsernameSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_service.update_username(user_id=user_id, body=body)

    except UserNameAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.patch(path="/update_name/{user_id}", response_model=UserProfileSchema)
async def update_name(
    user_id: Annotated[int, Depends(get_request_user_id)],
    body: UserUpdateNameSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update_name(user_id=user_id, body=body)


@router.patch(path="/update_email/{user_id}", response_model=UserProfileSchema)
async def update_email(
    user_id: Annotated[int, Depends(get_request_user_id)],
    body: UserUpdateEmailSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_service.update_email(user_id=user_id, body=body)
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.patch(path="/update_password/{user_id}", response_model=UserProfileSchema)
async def update_password(
    user_id: Annotated[int, Depends(get_request_user_id)],
    body: UserUpdatePasswordSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        return await user_service.update_password(user_id=user_id, body=body)

    except UserIncorrectPasswordException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)


@router.delete(path="/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: Annotated[int, Depends(get_request_user_id)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        await user_service.delete_user(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
