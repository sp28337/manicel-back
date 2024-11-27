import json
from dataclasses import dataclass

from redis import asyncio as Redis

from app.schemas.products_schema import ProductSchema


@dataclass
class ProductCache:
    redis_connection: Redis

    async def get_product(self, product_id: int) -> ProductSchema | None:
        async with self.redis_connection as r:
            if product_json := await r.get(product_id):
                return ProductSchema.model_validate(json.loads(product_json))

    async def set_product(self, product: ProductSchema | None):
        product_key = product.id
        if product_json := product.model_dump_json():
            async with self.redis_connection as r:
                await r.set(product_key, product_json)
                ttl_seconds = 60
                await r.expire(product_key, ttl_seconds)
                remaining_ttl = await r.ttl(product_key)
                print(
                    f"Оставшееся время жизни ключа '{product_key}': {remaining_ttl} секунд"
                )

    async def get_products(self) -> list[ProductSchema] | None:
        async with self.redis_connection as r:
            products_json = await r.lrange("products", 0, -1)
            return [
                ProductSchema.model_validate(json.loads(product))
                for product in products_json
            ]

    async def set_products(self, products: list[ProductSchema] | None):
        if products_json := [product.model_dump_json() for product in products]:
            async with self.redis_connection as r:
                list_key = "products"
                await r.lpush(
                    list_key,
                    *products_json,
                )
                # Установка времени жизни (TTL) для ключа в секундах
                ttl_seconds = 60  # 1 минута
                await r.expire(list_key, ttl_seconds)
                # Проверка оставшегося времени жизни
                remaining_ttl = await r.ttl(list_key)
                print(
                    f"Оставшееся время жизни ключа '{list_key}': {remaining_ttl} секунд"
                )
