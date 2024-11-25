from dataclasses import dataclass

from exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    PermissionDeniedException,
)
from repositories import ProductCache, ProductRepository, UserRepository
from schemas import ProductSchema, CreateProductSchema, UpdtaeProductSchema


@dataclass
class ProductService:

    product_repository: ProductRepository
    product_cache: ProductCache
    user_repository: UserRepository

    async def read_products(self) -> list[ProductSchema]:
        if cache_products := await self.product_cache.get_products():
            print("*" * 100)
            return cache_products
        else:
            print("-" * 100)
            products = await self.product_repository.read_products()
            products_schema = [
                ProductSchema.model_validate(product) for product in products
            ]
            # products_schema = [ProductsSchema(
            #     id=product.id,
            #     name=product.name,
            #     category=product.category,
            #     flavor=product.flavor,
            #     description=product.description,
            # ) for product in products]
            await self.product_cache.set_products(products_schema)
            return products_schema

    async def read_product(self, product_id: int) -> ProductSchema:
        if cache_product := await self.product_cache.get_product(product_id):
            print("*" * 100)
            return cache_product

        print("-" * 100)

        check_product = await self.product_repository.read_product_by_id(product_id)
        if check_product is None:
            raise ProductNotFoundException

        product = await self.product_repository.read_product_by_id(product_id)
        product_schema = ProductSchema.model_validate(product)
        # product_schema = ProductSchema(
        #     id=product.id,
        #     name=product.name,
        #     description=product.description,
        #     flavor=product.flavor,
        #     category=product.category,
        # )
        await self.product_cache.set_product(product_schema)
        return product_schema

    async def create_product(
        self, body: CreateProductSchema, user_id: int
    ) -> ProductSchema:
        await self._validate_admin(user_id)

        check_product = await self.product_repository.read_product_by_name(body.name)
        if check_product:
            raise ProductAlreadyExistsException

        product_id = await self.product_repository.create_product(body)
        new_product = await self.product_repository.read_product_by_id(product_id)
        return ProductSchema.model_validate(new_product)

    async def update_product_name(
        self, product_id: int, product_name: str, user_id: int
    ) -> UpdtaeProductSchema:
        await self._validate_admin(user_id)

        check_product = await self.product_repository.read_product_by_id(product_id)
        if check_product is None:
            raise ProductNotFoundException

        updated_product = await self.product_repository.update_product_name(
            product_id, product_name
        )
        return UpdtaeProductSchema.model_validate(updated_product)

    async def delete_product(self, product_id: int, user_id: int) -> None:
        await self._validate_admin(user_id)
        check_product = await self.product_repository.read_product_by_id(product_id)

        if check_product is None:
            raise ProductNotFoundException
        await self.product_repository.delete_product(product_id)

    async def _validate_admin(self, user_id: int) -> bool:
        user = await self.user_repository.read_user_by_id(user_id)
        print(f"\nuser_is_admin: {user.admin}\n")
        if user.admin is False:
            raise PermissionDeniedException
