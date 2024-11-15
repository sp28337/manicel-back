from fastapi import Depends

from sqlalchemy.orm import Session

from infrastructure.cache import get_redis_connection
from infrastructure.database import get_db_session
from repositories.product_cache_repository import ProductCache
from repositories.product_repository import ProductRepository
from services.product_service import ProductService


def get_product_repository(db_session: Session = Depends(get_db_session)) -> ProductRepository:
    return ProductRepository(db_session)


def get_product_cache_repository() -> ProductCache:
    redis_connection = get_redis_connection()
    return ProductCache(redis_connection)


def get_product_service(
    product_repository: ProductRepository = Depends(get_product_repository),
    product_cache: ProductCache = Depends(get_product_cache_repository)
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        product_cache=product_cache
    )
