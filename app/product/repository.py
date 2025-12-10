import logging

from fastapi import HTTPException, status
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.schemas import ProductCatalogSchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app.product.models import Product, Category


class ProductRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def ping_db(self) -> None:
        async with self.db_session as session:
            try:
                await session.execute(text("SELECT 1"))
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database is not available",
                )
            return {"text": "db is working"}

    async def get_products(self) -> list[Product] | None:
        stmt = select(Product).order_by(Product.id)
        result = await self.db_session.execute(stmt)
        products = result.unique().scalars().all()

        return products

    async def get_catalog_products(self) -> list[ProductCatalogSchema] | None:
        stmt = (
            select(
                Product.id,
                Product.name,
                Product.name_ru,
                Product.articule,
                Category.name.label("type"),
            )
            .join(Product.category)
            .order_by(Product.id)
        )
        result = await self.db_session.execute(stmt)
        products = result.unique().all()
        return products

    async def get_product_by_name(self, product_name: str) -> Product | None:
        stmt = select(Product).where(Product.name == product_name)
        result = await self.db_session.execute(stmt)
        product = result.scalars().first()
        return product

    async def get_product_by_id(self, product_id: int) -> Product | None:
        product = await self.db_session.get(Product, product_id)
        return product

    async def create_product(self, body: Product, uid: int) -> int:
        new_product = Product(
            uid=uid,
            status=body.status,
            articule=body.articule,
            name=body.name,
            name_ru=body.name_ru,
            description=body.description,
            flavor_id=body.flavor_id,
            category_id=body.category_id,
            complectation_id=body.complectation_id,
            reviews=body.reviews,
            attention=body.attention,
            expiration_date_id=body.expiration_date_id,
            note=body.note,
        )
        self.db_session.add(new_product)
        await self.db_session.flush()
        product_id = new_product.id
        await self.db_session.commit()
        logging.info(f"[DB] created new product id:{product_id}")
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
        return await self.get_product_by_id(product_id)

    async def delete_product(self, product_id: int) -> None:
        await self.db_session.execute(delete(Product).filter(Product.id == product_id))
        await self.db_session.commit()
