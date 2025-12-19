from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.bestsellers.schemas import BestsellersSchema
from app.product.models import Product, Category, Flavor, Ingredient


class BestsellersRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_bestsellers(self) -> list[BestsellersSchema]:
        stmt = (
            select(
                Product.articule,
                Product.id,
                Product.name,
                Product.name_ru,
                Product.reviews,
                func.array_agg(Ingredient.name).label("ingredients"),
                Category.name.label("type"),
            )
            .join(Product.category)
            .join(Product.flavor)
            .join(Flavor.ingredients)
            .group_by(Product.id, Category.name, Product.name, Product.reviews)
            .order_by(Product.reviews.desc())
            .limit(5)
        )
        result = await self.db_session.execute(stmt)
        bestsellers = result.all()

        return bestsellers
