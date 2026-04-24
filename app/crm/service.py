from dataclasses import dataclass

from app.crm.models import LeadStatus
from app.crm.repository import CRMRepository
from app.crm.schemas import LeadCreateSchema, LeadSchema, LeadUpdateSchema
from app.exceptions import (
    LeadNotFoundException,
    PermissionDeniedException,
    UserNotFoundException,
)
from app.user.repository import UserRepository


@dataclass
class CRMService:
    crm_repository: CRMRepository
    user_repository: UserRepository

    async def create_lead(self, body: LeadCreateSchema) -> LeadSchema:
        lead = await self.crm_repository.create_lead(body)
        return LeadSchema.model_validate(lead)

    async def get_leads(
        self, user_id: int, status: LeadStatus | None
    ) -> list[LeadSchema]:
        await self._validate_admin(user_id)
        leads = await self.crm_repository.get_leads(status=status)
        return [LeadSchema.model_validate(lead) for lead in leads]

    async def update_lead(
        self, lead_id: int, user_id: int, body: LeadUpdateSchema
    ) -> LeadSchema:
        await self._validate_admin(user_id)
        lead = await self.crm_repository.get_lead_by_id(lead_id)
        if not lead:
            raise LeadNotFoundException

        if body.assigned_manager_id is not None:
            manager = await self.user_repository.read_user_by_id(
                body.assigned_manager_id
            )
            if manager is None:
                raise UserNotFoundException

        updated_lead = await self.crm_repository.update_lead(lead_id=lead_id, body=body)
        return LeadSchema.model_validate(updated_lead)

    async def _validate_admin(self, user_id: int) -> None:
        user = await self.user_repository.read_user_by_id(user_id)
        if user is None or not user.admin:
            raise PermissionDeniedException
