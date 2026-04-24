from typing import Annotated

from fastapi import Depends, security, Security, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import (
    TokenExpiredException,
    IncorrectTokenException,
)
from app.settings import get_settings
from app.infrastructure.database_accessor import get_async_db_session
from app.product.repository import ProductRepository
from app.product.service import ProductService
from app.bestsellers.repository import BestsellersRepository
from app.bestsellers.service import BestsellersService
from app.search.repository import SearchRepository
from app.search.service import SearchService
from app.user.auth.clients import GoogleClient, YandexClient
from app.user.auth.service import AuthService
from app.user.service import UserService
from app.user.repository import UserRepository
from app.crm.repository import CRMRepository
from app.crm.service import CRMService
from app.admin.repository import AdminRepository
from app.admin.service import AdminService

settings = get_settings()


# Get repositories ----------------------------------------------------------------------------------------------------
async def get_product_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> ProductRepository:
    return ProductRepository(db_session=db_session)


async def get_search_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> SearchRepository:
    return SearchRepository(db_session=db_session)


async def get_bestsellers_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> BestsellersRepository:
    return BestsellersRepository(db_session=db_session)


async def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_crm_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> CRMRepository:
    return CRMRepository(db_session=db_session)


async def get_admin_repository(
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> AdminRepository:
    return AdminRepository(db_session=db_session)


# Get clients ---------------------------------------------------------------------------------------------------------


async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=settings)


async def get_yandex_client() -> YandexClient:
    return YandexClient(settings=settings)


# Get services --------------------------------------------------------------------------------------------------------
async def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        user_repository=user_repository,
    )


async def get_bestsellers_service(
    bestsellers_repository: Annotated[
        BestsellersRepository, Depends(get_bestsellers_repository)
    ],
) -> BestsellersService:
    return BestsellersService(
        bestsellers_repository=bestsellers_repository,
    )


async def get_search_service(
    search_repository: Annotated[SearchRepository, Depends(get_search_repository)],
) -> SearchService:
    return SearchService(
        search_repository=search_repository,
    )


async def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    google_client: Annotated[GoogleClient, Depends(get_google_client)],
    yandex_client: Annotated[YandexClient, Depends(get_yandex_client)],
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client,
        yandex_client=yandex_client,
    )


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


async def get_crm_service(
    crm_repository: Annotated[CRMRepository, Depends(get_crm_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> CRMService:
    return CRMService(crm_repository=crm_repository, user_repository=user_repository)


async def get_admin_service(
    admin_repository: Annotated[AdminRepository, Depends(get_admin_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AdminService:
    return AdminService(
        admin_repository=admin_repository,
        user_repository=user_repository,
    )


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
