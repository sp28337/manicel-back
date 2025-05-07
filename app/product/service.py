from dataclasses import dataclass

from app.exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    PermissionDeniedException,
)
from app.product.repository.cache import ProductCache
from app.product.repository.database import ProductRepository
from app.user.repository import UserRepository
from app.product.schemas import (
    ProductSchema,
    CreateProductSchema,
    UpdtaeProductSchema,
    ProductCatalogSchema,
    BestsellerSchema,
)


@dataclass
class ProductService:

    product_repository: ProductRepository
    product_cache: ProductCache
    user_repository: UserRepository
    __CACHE = True

    async def get_bestsellers(self) -> list[BestsellerSchema]:
        if cache_bestsellers := await self.product_cache.get_bestsellers():
            print("*" * 100)
            return cache_bestsellers
        else:
            print("-" * 100)
            bestsellers = await self.product_repository.get_bestsellers()
            bestsellers_schema = [
                BestsellerSchema.model_validate(bestseller)
                for bestseller in bestsellers
            ]
            if self.__CACHE:
                await self.product_cache.set_bestsellers(bestsellers_schema)
            else:
                print(f"\n\n\nNOCACHE\n\n\n")

            return bestsellers_schema

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
            if self.__CACHE:
                await self.product_cache.set_products(products_schema)
            else:
                print(f"\n\n\nNOCACHE\n\n\n")
            return products_schema

    async def read_catalog_products(self) -> list[ProductCatalogSchema]:
        if cache_catalog_products := await self.product_cache.get_catalog_products():
            print("*" * 100)
            return cache_catalog_products
        else:
            print("-" * 100)
            catalog_products = await self.product_repository.read_catalog_products()
            print("**********************")
            print(product for product in catalog_products)
            products_catalog_schema = [
                ProductCatalogSchema.model_validate(product)
                for product in catalog_products
            ]
            # products_schema = [ProductsSchema(
            #     id=product.id,
            #     name=product.name,
            #     category=product.category,
            #     flavor=product.flavor,
            #     description=product.description,
            # ) for product in products]

            if self.__CACHE:
                await self.product_cache.set_catalog_products(products_catalog_schema)
            else:
                print(f"\n\n\nNOCACHE\n\n\n")

            return products_catalog_schema

    async def search_products(self, query: str) -> list[ProductCatalogSchema]:
        # if cache_catalog_products := await self.product_cache.get_catalog_products():
        #     print("*" * 100)
        #     return cache_catalog_products
        # else:
        print("-" * 100)
        search_products = await self.product_repository.search_products(query)
        print("**********************")
        print(product for product in search_products)
        products_search_schema = [
            ProductCatalogSchema.model_validate(product) for product in search_products
        ]
        # products_schema = [ProductsSchema(
        #     id=product.id,
        #     name=product.name,
        #     category=product.category,
        #     flavor=product.flavor,
        #     description=product.description,
        # ) for product in products]

        if self.__CACHE:
            await self.product_cache.set_catalog_products(products_search_schema)
        else:
            print(f"\n\n\nNOCACHE\n\n\n")

        return products_search_schema

    async def read_product(self, product_id: int) -> ProductSchema:
        if cache_product := await self.product_cache.get_product(product_id):
            print("*" * 100)
            return cache_product

        print("-" * 100)

        product = await self.product_repository.read_product_by_id(product_id)
        if product is None:
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
        await self._validate_product_exists(body.name)
        print(f"\n\nbody: {body}\n\n")
        product_id = await self.product_repository.create_product(body)
        print(f"\n\nproduct_id: {product_id}\n\n")
        new_product = await self.product_repository.read_product_by_id(product_id)
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
        if user.admin is False:
            raise PermissionDeniedException

    async def _validate_product_exists(self, product_id_or_name: int | str):
        if type(product_id_or_name) is int:
            product = await self.product_repository.read_product_by_id(
                product_id_or_name
            )
            if product is None:
                raise ProductNotFoundException

        elif type(product_id_or_name) is str:
            product = await self.product_repository.read_product_by_name(
                product_id_or_name
            )
            if product:
                raise ProductAlreadyExistsException
