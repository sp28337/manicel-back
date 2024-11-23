from typing import Annotated

from fastapi import Depends, security, Security, HTTPException, status

from sqlalchemy.orm import Session

from clients import GoogleClient, YandexClient
from exceptions import (
    TokenExpiredException,
    IncorrectTokenException,
)
from infrastructure.cache import get_redis_connection
from infrastructure.database import get_db_session
from repositories import ProductCache, UserRepository, ProductRepository
from services import ProductService, UserService, AuthService
from settings import Settings


# Get repositories ----------------------------------------------------------------------------------------------------
def get_product_repository(
    db_session: Annotated[Session, Depends(get_db_session)]
) -> ProductRepository:
    return ProductRepository(db_session=db_session)


def get_product_cache_repository() -> ProductCache:
    redis_connection = get_redis_connection()
    return ProductCache(redis_connection=redis_connection)


def get_user_repository(
    db_session: Annotated[Session, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db_session=db_session)


# Get clients ---------------------------------------------------------------------------------------------------------
def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())


# Get services --------------------------------------------------------------------------------------------------------
def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    product_cache: Annotated[ProductCache, Depends(get_product_cache_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        product_cache=product_cache,
        user_repository=user_repository,
    )


def get_auth_service(
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


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


# Authorization -------------------------------------------------------------------------------------------------------
reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[
        security.http.HTTPAuthorizationCredentials, Security(reusable_oauth2)
    ],
) -> int:

    print(f"\ntoken credentials: {token.credentials}\n")

    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
        return user_id
    except TokenExpiredException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except IncorrectTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


# ---------------------------------------------------------------------------------------------------------------------
