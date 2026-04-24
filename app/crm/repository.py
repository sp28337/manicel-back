from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.crm.models import Lead, LeadStatus
from app.crm.schemas import LeadCreateSchema, LeadUpdateSchema


class CRMRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_lead(self, body: LeadCreateSchema) -> Lead:
        new_lead = Lead(**body.model_dump())
        self.db_session.add(new_lead)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_lead

    async def get_lead_by_id(self, lead_id: int) -> Lead | None:
        return await self.db_session.get(Lead, lead_id)

    async def get_leads(self, status: LeadStatus | None = None) -> list[Lead]:
        stmt = select(Lead).order_by(Lead.created_at.desc())
        if status:
            stmt = stmt.where(Lead.status == status)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def update_lead(self, lead_id: int, body: LeadUpdateSchema) -> Lead | None:
        values = body.model_dump(exclude_none=True)
        if not values:
            return await self.get_lead_by_id(lead_id)

        stmt = update(Lead).where(Lead.id == lead_id).values(**values)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return await self.get_lead_by_id(lead_id)
