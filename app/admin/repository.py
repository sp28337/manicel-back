from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crm.models import Lead, LeadStatus
from app.product.models import Product
from app.user.models import UserProfile


class AdminRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_users_total(self) -> int:
        result = await self.db_session.execute(select(func.count(UserProfile.id)))
        return int(result.scalar_one())

    async def get_admins_total(self) -> int:
        result = await self.db_session.execute(
            select(func.count(UserProfile.id)).where(UserProfile.admin.is_(True))
        )
        return int(result.scalar_one())

    async def get_products_total(self) -> int:
        result = await self.db_session.execute(select(func.count(Product.id)))
        return int(result.scalar_one())

    async def get_leads_total(self) -> int:
        result = await self.db_session.execute(select(func.count(Lead.id)))
        return int(result.scalar_one())

    async def get_new_leads_total(self) -> int:
        result = await self.db_session.execute(
            select(func.count(Lead.id)).where(Lead.status == LeadStatus.NEW)
        )
        return int(result.scalar_one())

    async def set_user_admin_flag(
        self, user_id: int, is_admin: bool
    ) -> UserProfile | None:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(admin=is_admin)
            .returning(UserProfile.id)
        )
        result = await self.db_session.execute(stmt)
        updated_user_id = result.scalar_one_or_none()
        if updated_user_id is None:
            return None

        await self.db_session.commit()
        return await self.db_session.get(UserProfile, updated_user_id)
