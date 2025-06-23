import logging

from dataclasses import dataclass

from app.exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    PermissionDeniedException,
)
from app.product.repository import ProductRepository
from app.user.repository import UserRepository
from app.product.schemas import (
    ProductSchema,
    CreateProductSchema,
    UpdtaeProductSchema,
    ProductCatalogSchema,
)


@dataclass
class ProductService:
    product_repository: ProductRepository
    user_repository: UserRepository

    async def get_products(self) -> list[ProductSchema]:
        products = await self.product_repository.get_products()
        logging.info("[DB] get_products")
        products_schema = [
            ProductSchema.model_validate(product) for product in products
        ]
        return products_schema

    async def get_catalog_products(self) -> list[ProductCatalogSchema]:
        catalog_products = await self.product_repository.get_catalog_products()
        logging.info("[DB] get_catalog_products")
        products_catalog_schema = [
            ProductCatalogSchema.model_validate(product)
            for product in catalog_products
        ]
        return products_catalog_schema

    async def get_product(self, product_id: int) -> ProductSchema:
        product = await self.product_repository.get_product_by_id(product_id)

        if product is None:
            raise ProductNotFoundException

        logging.info("[DB] get_product_by_id")
        product_schema = ProductSchema.model_validate(product)
        return product_schema

    async def create_product(
        self, body: CreateProductSchema, user_id: int
    ) -> ProductSchema:
        await self._validate_admin(user_id)
        await self._validate_product_exists(body.name)
        product_id = await self.product_repository.create_product(body=body, uid=user_id)
        new_product = await self.product_repository.get_product_by_id(product_id)
        return ProductSchema.model_validate(new_product)

    async def update_product_name(
        self, product_id: int, product_name: str, user_id: int
    ) -> UpdtaeProductSchema:
        await self._validate_admin(user_id)
        await self._validate_product_exists(product_id)
        updated_product = await self.product_repository.update_product_name(
            product_id, product_name
        )
        return UpdtaeProductSchema.model_validate(updated_product)

    async def delete_product(self, product_id: int, user_id: int) -> None:
        await self._validate_admin(user_id)
        await self._validate_product_exists(product_id)

        await self.product_repository.delete_product(product_id)

    async def _validate_admin(self, user_id: int) -> bool:
        user = await self.user_repository.read_user_by_id(user_id)
        print(f"\nuser_is_admin: {user.admin}\n")
        if not user.admin:
            raise PermissionDeniedException

    async def _validate_product_exists(self, product_id_or_name: int | str):
        if type(product_id_or_name) is int:
            product = await self.product_repository.get_product_by_id(
                product_id_or_name
            )
            if product is None:
                raise ProductNotFoundException

        elif type(product_id_or_name) is str:
            product = await self.product_repository.get_product_by_name(
                product_id_or_name
            )
            if product:
                raise ProductAlreadyExistsException
