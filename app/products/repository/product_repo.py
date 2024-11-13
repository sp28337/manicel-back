from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.models_1 import *
from app.products.schema import ProductsSchema, ProductSchema


class ProductRepository:
    def __init__(self, db_sesion: Session):
        self.db_session = db_sesion

    def read_products(self) -> list[Products] | None:
        with self.db_session as session:
            subquery = (
                session.query(
                    Flavors.name.label("flavor"),
                    func.aggregate_strings(Ingredients.name, ', ').label("ingredients")
                ).join(FlavorIngredients, Flavors.id == FlavorIngredients.flavor_id)
                .join(Ingredients, Ingredients.id == FlavorIngredients.ingredient_id)
                .group_by(Flavors.name)
                .subquery()
            )  # subquery - подзапрос для получения ингредиентов

            query = (
                session.query(
                    Products.name.label("name"),
                    Categories.name.label("category"),
                    Flavors.name.label("flavors"),
                    subquery.c.ingredients.label("ingredients"),
                    # Products.description.label("description")
                ).join(Categories, Products.category_id == Categories.id
                       ).join(Flavors, Flavors.id == Products.flavor_id
                              ).join(subquery, subquery.c.flavor == Flavors.name)
            )  # query - основной запрос для получения продуктов

            products: list[Products] = query.all()

        return products

    def read_product(self, product_name: str) -> ProductSchema | None:
        with self.db_session as session:
            sub_query = (
                session.query(
                    Flavors.name.label("flavor"),
                    func.aggregate_strings(Ingredients.name, ', ').label("ingredients")
                ).join(FlavorIngredients, Flavors.id == FlavorIngredients.flavor_id)
                .join(Ingredients, Ingredients.id == FlavorIngredients.ingredient_id)
                .group_by(Flavors.name)
                .subquery()
            )  # subquery - подзапрос для получения ингредиентов

            query = (
                session.query(
                    Products.name.label("name"),
                    Categories.name.label("category"),
                    Flavors.name.label("flavors"),
                    sub_query.c.ingredients.label("ingredients"),
                    Products.description.label("description")
                ).join(Categories, Products.category_id == Categories.id
                       ).join(Flavors, Flavors.id == Products.flavor_id
                              ).join(sub_query, sub_query.c.flavor == Flavors.name
                                     ).where(Flavors.name == product_name)
            )  # query - основной запрос для получения продукта

            product: ProductSchema = query.first()
        return product

