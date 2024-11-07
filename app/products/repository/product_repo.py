from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models_1 import *


class ProductRepository:
    def __init__(self, db_sesion: Session):
        self.db_session = db_sesion

    def get_products(self) -> list[Products] | None:

        with self.db_session as session:
            products: list[Products] = session.execute(select(Products)).scalars().all()
        return products

    def get_product(self, product_id: int) -> Products:
        query = select(Products).where(Products.id == product_id)
        with self.db_session as session:
            product: Products = session.execute(query).scalar_one_or_none()
            print(product)
        return product
