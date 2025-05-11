import json
import logging
from dataclasses import dataclass

from redis import asyncio as Redis

from app.product.schemas import ProductSchema, ProductCatalogSchema, BestsellerSchema

logging.basicConfig(
    # filename="py_log.log",
    level=logging.INFO,
    format=" * [%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    filemode="a"
)


@dataclass
class ProductCache:
    redis_connection: Redis

    async def get_product(self, product_id: int) -> ProductSchema | None:
        async with self.redis_connection as r:
            if product_json := await r.get(product_id):
                return ProductSchema.model_validate(json.loads(product_json))
            return None

    async def set_product(self, product: ProductSchema | None):
        product_key = product.id
        if product_json := product.model_dump_json():
            async with self.redis_connection as r:
                await r.set(product_key, product_json)
                ttl_seconds = 60
                await r.expire(product_key, ttl_seconds)
                remaining_ttl = await r.ttl(product_key)
                logging.info(f"[CHACHE] {product.name} cached for {remaining_ttl}s")

    async def get_bestsellers(self) -> list[BestsellerSchema] | None:
        async with self.redis_connection as r:
            bestsellers_json = await r.lrange("bestsellers", 0, -1)
            return [
                BestsellerSchema.model_validate(json.loads(bestseller))
                for bestseller in bestsellers_json
            ]

    async def set_bestsellers(self, bestsellers: list[BestsellerSchema] | None):
        if bestsellers_json := [
            bestseller.model_dump_json() for bestseller in bestsellers
        ]:
            async with self.redis_connection as r:
                list_key = "bestsellers"
                await r.lpush(
                    list_key,
                    *bestsellers_json,
                )
                ttl_seconds = 60  # 1 минута
                await r.expire(list_key, ttl_seconds)
                remaining_ttl = await r.ttl(list_key)
                logging.info(f"[CHACHE] bestsellers cached for {remaining_ttl}s")

    async def get_products(self) -> list[ProductSchema] | None:
        async with self.redis_connection as r:
            products_json = await r.lrange("products", 0, -1)
            return [
                ProductSchema.model_validate(json.loads(product))
                for product in products_json
            ]

    async def set_products(self, products: list[ProductSchema] | None):
        if set_products_json := [product.model_dump_json() for product in products]:
            async with self.redis_connection as r:
                list_key = "products"
                await r.lpush(
                    list_key,
                    *set_products_json,
                )
                # Установка времени жизни (TTL) для ключа в секундах
                ttl_seconds = 60  # 1 минута
                await r.expire(list_key, ttl_seconds)
                # Проверка оставшегося времени жизни
                remaining_ttl = await r.ttl(list_key)
                logging.info(f"[CHACHE] products cached for {remaining_ttl}s")

    async def get_catalog_products(self) -> list[ProductCatalogSchema] | None:
        async with self.redis_connection as r:
            catalog_products_json = await r.lrange("catalog_products", 0, -1)
            return [
                ProductCatalogSchema.model_validate(json.loads(product))
                for product in catalog_products_json
            ]

    async def set_catalog_products(
        self, catalog_products: list[ProductCatalogSchema] | None
    ):
        if catalog_products_json := [
            product.model_dump_json() for product in catalog_products
        ]:
            async with self.redis_connection as r:
                list_key = "catalog_products"
                await r.lpush(
                    list_key,
                    *catalog_products_json,
                )
                # Установка времени жизни (TTL) для ключа в секундах
                ttl_seconds = 60  # 1 минута
                await r.expire(list_key, ttl_seconds)
                # Проверка оставшегося времени жизни
                remaining_ttl = await r.ttl(list_key)
                logging.info(f"[CHACHE] catalog_products cached for {remaining_ttl}s")
