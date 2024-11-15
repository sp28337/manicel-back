import json
from dataclasses import dataclass
from typing import List

import redis as Redis

from schemas.products_schema import ProductSchema


@dataclass
class ProductCache:
    redis_connection: Redis

    def get_product(self, product_id: int) -> ProductSchema | None:
        with self.redis_connection as r:
            if product_json := r.get(product_id):
                return ProductSchema.model_validate(json.loads(product_json))

    def set_product(self, product: ProductSchema | None):
        product_key = product.id
        if product_json := product.model_dump_json():
            with self.redis_connection as r:
                r.set(product_key, product_json)
                ttl_seconds = 60
                r.expire(product_key, ttl_seconds)
                remaining_ttl = r.ttl(product_key)
                print(f"Оставшееся время жизни ключа '{product_key}': {remaining_ttl} секунд")

    def get_products(self) -> List[ProductSchema] | None:
        with self.redis_connection as r:
            products_json = r.lrange("products", 0, -1)
            return [ProductSchema.model_validate(json.loads(product)) for product in products_json]

    def set_products(self, products: List[ProductSchema] | None):
        if products_json := [product.model_dump_json() for product in products]:
            with self.redis_connection as r:
                list_key = "products"
                r.lpush(list_key, *products_json, )
                # Установка времени жизни (TTL) для ключа в секундах
                ttl_seconds = 60  # 1 минута
                r.expire(list_key, ttl_seconds)
                # Проверка оставшегося времени жизни
                remaining_ttl = r.ttl(list_key)
                print(f"Оставшееся время жизни ключа '{list_key}': {remaining_ttl} секунд")
