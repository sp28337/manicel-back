from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from app.dependencies import get_auth_service
from app.exceptions import UserNotFoundException, UserIncorrectPasswordException
from app.user.schemas import UserSchema
from app.user.auth.schemas import UserLoginSchema
from app.user.auth.service import AuthService
from app.settings import Settings

router = APIRouter(prefix="/auth", tags=["auth"])
settings = Settings()


@router.post(path="/login", response_model=UserLoginSchema)
async def login(
    body: UserSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return await auth_service.login(username=body.username, password=body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except UserIncorrectPasswordException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@router.get(path="/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(path="/login/yandex", response_class=RedirectResponse)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(path="/google")
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    user_data = await auth_service.google_auth(code=code)
    redirect = RedirectResponse(settings.CALLBACK_REDIRECT_URI)
    redirect.set_cookie(
        key="session",
        domain=settings.COOKIES_DOMAIN,
        value=user_data.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
    redirect.set_cookie(
        key="id",
        domain=settings.COOKIES_DOMAIN,
        value=user_data.user_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
    return redirect


@router.get(path="/yandex")
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    user_data = await auth_service.yandex_auth(code=code)
    redirect = RedirectResponse(settings.CALLBACK_REDIRECT_URI)
    redirect.set_cookie(
        key="session",
        domain=settings.COOKIES_DOMAIN,
        value=user_data.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
    redirect.set_cookie(
        key="id",
        domain=settings.COOKIES_DOMAIN,
        value=user_data.user_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
    return redirect
