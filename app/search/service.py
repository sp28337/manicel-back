import logging
from dataclasses import dataclass

from app.search.repository import SearchRepository
from app.search.schemas import SearchSchema


@dataclass
class SearchService:
    search_repository: SearchRepository

    async def get_search_products(self, query: str) -> list[SearchSchema]:
        search_products = await self.search_repository.get_search_products(query)
        logging.info("[DB] get_search_products")
        search_products_schema = [
            SearchSchema.model_validate(product) for product in search_products
        ]

        return search_products_schema
