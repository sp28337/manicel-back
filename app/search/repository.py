import logging

from sqlalchemy import select, or_, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.models import Product, Category
from app.search.schemas import SearchSchema


class SearchRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_search_products(
        self, query: str
    ) -> list[SearchSchema] | SearchSchema:
        logging.info(f"[QUERY] {query}")

        if query == "":
            return []

        query_string = f"%{query}%"

        stmt = (
            select(
                Product.id,
                Product.name,
                Product.name_ru,
                Product.articule,
                Category.name.label("type"),
            )
            .join(Product.category)
            .where(
                or_(
                    Product.name.ilike(query_string),
                    Product.name_ru.ilike(query_string),
                    cast(Product.reviews, String).ilike(query_string),
                )
            )
            .order_by(Product.name)
            .limit(5)
        )

        result = await self.db_session.execute(stmt)
        invoices = result.all()
        return invoices
