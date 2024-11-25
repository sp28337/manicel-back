from dataclasses import dataclass

from sqlalchemy import update, select

from infrastructure.database import LocalAsyncSession
from models.product_models import Product


@dataclass
class ProductRepository:
    db_session: LocalAsyncSession

    async def read_products(self) -> list[Product] | None:
        async with self.db_session() as session:
            # subquery = (
            #     session.query(
            #         Flavor.name.label("flavor"),
            #         func.aggregate_strings(Ingredient.name, ', ').label("ingredients")
            #     ).join(flavor_ingredients, Flavor.id == flavor_ingredients.c.flavor_id)
            #     .join(Ingredient, Ingredient.id == flavor_ingredients.c.ingredient_id)
            #     .group_by(Flavor.name)
            #     .subquery()
            # )  # subquery - подзапрос для получения ингредиентов
            #
            # query = (
            #     session.query(
            #         Product.name.label("name"),
            #         Category.name.label("category"),
            #         Flavor.name.label("flavors"),
            #         subquery.c.ingredients.label("ingredients"),
            #         # Products.description.label("description")
            #     ).join(Category, Product.category_id == Category.id
            #            ).join(Flavor, Flavor.id == Product.flavor_id
            #                   ).join(subquery, subquery.c.flavor == Flavor.name)
            # )  # query - основной запрос для получения продуктов
            #
            # products: list[Product] = query.all()
            products = (await session.execute(select(Product).order_by(Product.id))).unique().scalars().all()
            print(products)
            return products

    async def read_product_by_name(self, product_name: str) -> Product | None:
        async with self.db_session() as session:
            product = (
                await session.query(Product)
                .filter(Product.name == product_name)
                .first()
            )
            print(product)
            return product

    async def read_product_by_id(self, product_id: int) -> Product | None:
        async with self.db_session() as session:
            # sub_query = (
            #     session.query(
            #         Flavor.name.label("flavor"),
            #         func.aggregate_strings(Ingredient.name, ', ').label("ingredients")
            #     ).join(flavor_ingredients, Flavor.id == flavor_ingredients.c.flavor_id)
            #     .join(Ingredient, Ingredient.id == flavor_ingredients.c.ingredient_id)
            #     .group_by(Flavor.name)
            #     .subquery()
            # )  # subquery - подзапрос для получения ингредиентов
            #
            # query = (
            #     session.query(
            #         Product.name.label("name"),
            #         Category.name.label("category"),
            #         Flavor.name.label("flavors"),
            #         sub_query.c.ingredients.label("ingredients"),
            #         Product.description.label("description")
            #     ).join(Category, Product.category_id == Category.id
            #            ).join(Flavor, Flavor.id == Product.flavor_id
            #                   ).join(sub_query, sub_query.c.flavor == Flavor.name
            #                          ).where(Flavor.name == flavor_name)
            # )  # query - основной запрос для получения продукта
            #
            #                       or
            #
            # product = session.query(Product).filter(Product.id == product_id).first()
            #
            #                       or
            product = await session.get(Product, product_id)
            print(product)
            return product

    async def create_product(self, body: Product) -> int:
        async with self.db_session() as session:
            new_product = Product(
                name=body.name,
                description=body.description,
                category_id=body.category_id,
                flavor_id=body.flavor_id,
            )
            await session.add(new_product)
            await session.flush()
            product_id = new_product.id
            await session.commit()
            return product_id

    async def update_product_name(self, product_id: int, product_name: str) -> Product:
        async with self.db_session() as session:
            stmt = (
                update(Product)
                .where(Product.id == product_id)
                .values(name=product_name)
                .returning(Product.id)
            )
            product_id = (await session.execute(stmt)).scalar_one_or_none()
            await session.commit()
            await session.flush()
            return await self.read_product_by_id(product_id)

    async def delete_product(self, product_id: int) -> None:
        async with self.db_session() as session:
            await session.query(Product).filter(Product.id == product_id).delete()
            await session.commit()
