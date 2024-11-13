from dataclasses import dataclass

from app.products.repository import ProductRepository
from app.products.schema import ProductsSchema, ProductSchema


@dataclass
class ProductService:

    product_repository: ProductRepository
    # product_cache: None

    def read_products(self) -> list[ProductsSchema]:
        # if cache_product := self.product_cache.read_products():
        #     return cache_products
        # else:
        products = self.product_repository.read_products()
        # product_schema = [ProductsSchema.model_validate(product) for product in products]
        products_schema = [ProductsSchema(
            name=product.name,
            category=product.category,
            flavor=product.flavors,
            ingredients=product.ingredients,
            # description=product.description,
        ) for product in products]
        print(products_schema)
        # self.product_cache.write_items(product_schema)
        return products_schema

    def read_product(self, product_name: str) -> ProductSchema:
        product = self.product_repository.read_product(product_name)
        product_schema = ProductSchema(
            name=product.name,
            category=product.category,
            flavor=product.flavors,
            ingredients=product.ingredients,
            description=product.description,
        )
        # print('*********************************', product_schema)
        return product_schema

