import logging

from dataclasses import dataclass

from app.bestsellers.repository import BestsellersRepository
from app.bestsellers.schemas import BestsellersSchema

logger = logging.getLogger(__name__)


@dataclass
class BestsellersService:
    bestsellers_repository: BestsellersRepository

    async def get_bestsellers(self) -> list[BestsellersSchema]:
        logging.info("[DB] get_bestsellers")
        bestsellers = await self.bestsellers_repository.get_bestsellers()
        bestsellers_schema = [
            BestsellersSchema.model_validate(bestseller) for bestseller in bestsellers
        ]
        return bestsellers_schema
