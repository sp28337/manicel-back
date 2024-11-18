from typing import Annotated

from fastapi import Depends, security, Security, HTTPException

from sqlalchemy.orm import Session

from exceptions import TokenExpiredException, IncorrectTokenException, PermissionDeniedException
from infrastructure.cache import get_redis_connection
from infrastructure.database import get_db_session
from repositories import ProductCache, UserRepository, ProductRepository
from services import ProductService, UserService, AuthService
from settings import Settings


def get_product_repository(
        db_session: Annotated[Session, Depends(get_db_session)]
) -> ProductRepository:
    return ProductRepository(db_session=db_session)


def get_product_cache_repository() -> ProductCache:
    redis_connection = get_redis_connection()

    return ProductCache(redis_connection=redis_connection)


def get_product_service(
        product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
        product_cache: Annotated[ProductCache, Depends(get_product_cache_repository)]
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        product_cache=product_cache
    )


def get_user_repository(
        db_session: Annotated[Session, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings())


def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


    return UserService(user_repository=user_repository)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:

    return AuthService(user_repository=user_repository)
