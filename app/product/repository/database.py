from sqlalchemy import update, select, delete, func, or_, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.schemas import ProductCatalogSchema, BestsellerSchema

from app.product.models import Product, Category, Flavor, Ingredient


class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_bestsellers(self) -> list[BestsellerSchema]:
        stmt = select(
            Product.id,
            Product.name,
            Product.name_ru,
            Product.reviews,
            func.array_agg(Ingredient.name).label("ingredients"),
            Category.name.label("type")
        ).join(Product.category).join(Product.flavor).join(Flavor.ingredients).group_by(Product.id, Category.name, Product.name, Product.reviews).order_by(Product.reviews.desc()).limit(5)
        print(stmt)
        result = await self.db_session.execute(stmt)
        bestsellers = result.all()

        print(f"\n\n\n{bestsellers}\n\n\n")

        for row in bestsellers:
            print(row)

        return bestsellers

    async def read_products(self) -> list[Product] | None:
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
        stmt = select(Product).order_by(Product.id)
        result = await self.db_session.execute(stmt)
        products = result.unique().scalars().all()
        print(f"\n *** products: {products}\n")

        return products

    async def read_catalog_products(self) -> list[ProductCatalogSchema] | None:
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
        stmt = (
                select(
                    Product.id,
                    Product.name,
                    Product.name_ru,
                    Product.articule,
                    Category.name.label("type")
                ).join(Product.category).order_by(Product.id)
        )
        result = await self.db_session.execute(stmt)
        products = result.unique().all()
        print(f"\n *** products: {products}\n")
        return products

    async def search_products(self, query: str) -> list[ProductCatalogSchema] | ProductCatalogSchema:
        if query == "":
            return []

        query_string = f"%{query}%"

        print(f"\n\n\nquery_string: {query_string}\n\n\n")

        stmt = (
            select(
                Product.id,
                Product.name,
                Product.name_ru,
                Product.articule,
                Category.name.label("type")
            ).join(Product.category)
            .where(
                or_(
                    Product.name.ilike(query_string),
                    Product.name_ru.ilike(query_string),
                    cast(Product.reviews, String).ilike(query_string),
                )
            )
            .order_by(Product.name).limit(5)
        )

        result = await self.db_session.execute(stmt)
        print(f"\n *** result: {result}\n")
        invoices = result.all()
        print(f"\n *** invoices: {invoices}\n")
        return invoices

    async def read_product_by_name(self, product_name: str) -> Product | None:
        stmt = select(Product).where(Product.name == product_name)
        result = await self.db_session.execute(stmt)
        print(f"\n *** result: {result}\n")
        product = result.scalars().first()
        print(f"\n *** product: {product}\n")
        return product

    async def read_product_by_id(self, product_id: int) -> Product | None:
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
        product = await self.db_session.get(Product, product_id)
        return product

    async def create_product(self, body: Product) -> int:
        new_product = Product(
            name=body.name,
            description=body.description,
            category_id=body.category_id,
            flavor_id=body.flavor_id,
        )
        self.db_session.add(new_product)
        await self.db_session.flush()
        product_id = new_product.id
        await self.db_session.commit()
        return product_id

    async def update_product_name(self, product_id: int, product_name: str) -> Product:
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(name=product_name)
            .returning(Product.id)
        )
        result = await self.db_session.execute(stmt)
        product_id = result.scalar_one_or_none()

        await self.db_session.commit()
        await self.db_session.flush()
        return await self.read_product_by_id(product_id)

    async def delete_product(self, product_id: int) -> None:
        await self.db_session.execute(delete(Product).filter(Product.id == product_id))
        await self.db_session.commit()
