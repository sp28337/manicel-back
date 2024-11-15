from sqlalchemy import update
from sqlalchemy.orm import Session

from models.product_models import *
from schemas.products_schema import ProductSchema, CreateProductSchema


class ProductRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def read_products(self) -> list[Product] | None:
        with self.db_session as session:
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
            products = session.query(Product).all()
            print(products)
        return products

    def read_product(self, product_id: int) -> ProductSchema | None:
        with self.db_session as session:
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

            product = session.query(Product).filter(Product.id == product_id).first()
            print(product)
        return product

    def create_product(self, body: CreateProductSchema) -> int:
        with self.db_session as session:
            new_product = Product(
                name=body.name,
                description=body.description,
                category_id=body.category_id,
                flavor_id=body.flavor_id
            )
            session.add(new_product)
            session.flush()
            product_id = new_product.id
            session.commit()
        return product_id

    def update_product_name(self, product_id: int, product_name: str) -> Product:
        with self.db_session as session:
            stmt = update(Product).where(Product.id == product_id).values(name=product_name).returning(Product.id)
            product_id = session.execute(stmt).scalar_one_or_none()
            session.commit()
            session.flush()
            return self.read_product(product_id)

    def delete_product(self, product_id: int) -> None:
        with self.db_session as session:
            session.query(Product).filter(Product.id == product_id).delete()
            session.commit()
