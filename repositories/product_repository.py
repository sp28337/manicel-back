from dataclasses import dataclass

from sqlalchemy import update

from infrastructure.database import LocalSession
from models.product_models import Product


@dataclass
class ProductRepository:
    db_session: LocalSession

    def read_products(self) -> list[Product] | None:
        with self.db_session() as session:
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
            products = session.query(Product).order_by(Product.id).all()
            print(products)
            return products

    def read_product_by_name(self, product_name: str) -> Product | None:
        with self.db_session() as session:
            product = session.query(Product).filter(Product.name == product_name).first()
            print(product)
            return product

    def read_product_by_id(self, product_id: int) -> Product | None:
        with self.db_session() as session:
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
            product = session.get(Product, product_id)
            print(product)
            return product

    def create_product(self, body: Product) -> int:
        with self.db_session() as session:
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
        with self.db_session() as session:
            stmt = update(Product).where(Product.id == product_id).values(name=product_name).returning(Product.id)
            product_id = session.execute(stmt).scalar_one_or_none()
            session.commit()
            session.flush()
            return self.read_product_by_id(product_id)

    def delete_product(self, product_id: int) -> None:
        with self.db_session() as session:
            session.query(Product).filter(Product.id == product_id).delete()
            session.commit()
