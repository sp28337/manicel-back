from dataclasses import dataclass

from app.products.repository import ProductRepository
from app.products.schema import ProductsSchema


@dataclass
class ProductService:

    product_repository: ProductRepository
    # product_cache: None

    def get_products(self) -> list[ProductsSchema]:
        # if cache_product := self.product_cache.read_products():
        #     return cache_products
        # else:
        products = self.product_repository.get_products()
        product_schema = [ProductsSchema.model_validate(product) for product in products]
        print(product_schema)
        # self.product_cache.write_items(product_schema)
        return product_schema

    def get_product(self, product_id: int) -> ProductsSchema:
        product = self.product_repository.get_product(product_id)
        print(product)
        return product
