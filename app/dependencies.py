from typing import Annotated

from fastapi import Depends, security, Security, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.user.auth.clients import GoogleClient, YandexClient
from app.exceptions import (
    TokenExpiredException,
    IncorrectTokenException,
)
from app.infrastructure.cache_accessor import get_redis_connection
from app.infrastructure.database_accessor import get_async_db_session
from app.product.repository import ProductCache, ProductRepository
from app.product.service import ProductService
from app.user.auth.service import AuthService
from app.user.service import UserService
from app.user.repository import UserRepository

from app.settings import Settings


# Get repositories ----------------------------------------------------------------------------------------------------
async def get_product_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> ProductRepository:
    return ProductRepository(db_session=db_session)


async def get_product_cache_repository() -> ProductCache:
    redis_connection = get_redis_connection()
    return ProductCache(redis_connection=redis_connection)


async def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> UserRepository:
    return UserRepository(db_session=db_session)


# Get clients ---------------------------------------------------------------------------------------------------------

async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


async def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())


# Get services --------------------------------------------------------------------------------------------------------
async def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    product_cache: Annotated[ProductCache, Depends(get_product_cache_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        product_cache=product_cache,
        user_repository=user_repository,
    )


async def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    google_client: Annotated[GoogleClient, Depends(get_google_client)],
    yandex_client: Annotated[YandexClient, Depends(get_yandex_client)],
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


# Authorization -------------------------------------------------------------------------------------------------------
reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[
        security.http.HTTPAuthorizationCredentials, Security(reusable_oauth2)
    ],
) -> int:

    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
        return user_id
    except TokenExpiredException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except IncorrectTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


# ---------------------------------------------------------------------------------------------------------------------
