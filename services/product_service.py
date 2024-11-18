from dataclasses import dataclass

from exceptions import ProductNotFoundException, ProductAlreadyExistsException
from repositories import ProductCache, ProductRepository
from schemas import ProductSchema, CreateProductSchema, UpdtaeProductSchema


@dataclass
class ProductService:

    product_repository: ProductRepository
    product_cache: ProductCache

    def read_products(self) -> list[ProductSchema]:
        if cache_products := self.product_cache.get_products():
            print('*' * 100)
            return cache_products
        else:
            print('-' * 100)
            products = self.product_repository.read_products()
            products_schema = [ProductSchema.model_validate(product) for product in products]
            # products_schema = [ProductsSchema(
        #     id=product.id,
        #     name=product.name,
        #     category=product.category,
        #     flavor=product.flavor,
        #     description=product.description,
        # ) for product in products]
            self.product_cache.set_products(products_schema)
            return products_schema

    def read_product(self, product_id: int) -> ProductSchema:
        if cache_product := self.product_cache.get_product(product_id):
            print('*' * 100)
            return cache_product

        print('-' * 100)

        check_product = self.product_repository.read_product_by_id(product_id)
        if check_product is None:
            raise ProductNotFoundException

        product = self.product_repository.read_product_by_id(product_id)
        product_schema = ProductSchema.model_validate(product)
        # product_schema = ProductSchema(
        #     id=product.id,
        #     name=product.name,
        #     description=product.description,
        #     flavor=product.flavor,
        #     category=product.category,
        # )
        self.product_cache.set_product(product_schema)
        return product_schema

    def create_product(self, body: CreateProductSchema) -> ProductSchema:
        check_product = self.product_repository.read_product_by_name(body.name)
        if check_product:
            raise ProductAlreadyExistsException

        product_id = self.product_repository.create_product(body)
        new_product = self.product_repository.read_product_by_id(product_id)
        return ProductSchema.model_validate(new_product)

    def update_product_name(self, product_id: int, product_name: str) -> UpdtaeProductSchema:
        check_product = self.product_repository.read_product_by_id(product_id)

        if check_product is None:
            raise ProductNotFoundException

        updated_product = self.product_repository.update_product_name(product_id, product_name)
        return UpdtaeProductSchema.model_validate(updated_product)

    def delete_product(self, product_id: int) -> None:
        check_product = self.product_repository.read_product_by_id(product_id)

        if check_product is None:
            raise ProductNotFoundException
        self.product_repository.delete_product(product_id)
