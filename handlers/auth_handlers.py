from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
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
        return auth_service.login(body.password, body.username)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )


@router.get(
    path="/login/google",
    response_class=RedirectResponse
)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    path="/login/yandex",
    response_class=RedirectResponse
)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(path="/google")
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.google_auth(code=code)


@router.get(path="/yandex")
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    print(f"\n1) Код, который yandex присылает для второго запроса\ncode: {code}\n")
    return auth_service.yandex_auth(code=code)
