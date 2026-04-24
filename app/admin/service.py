from dataclasses import dataclass

from app.admin.repository import AdminRepository
from app.admin.schemas import DashboardSchema
from app.exceptions import PermissionDeniedException, UserNotFoundException
from app.user.repository import UserRepository
from app.user.schemas import UserProfileSchema


@dataclass
class AdminService:
    admin_repository: AdminRepository
    user_repository: UserRepository

    async def get_dashboard(self, user_id: int) -> DashboardSchema:
        await self._validate_admin(user_id)
        return DashboardSchema(
            users_total=await self.admin_repository.get_users_total(),
            admins_total=await self.admin_repository.get_admins_total(),
            products_total=await self.admin_repository.get_products_total(),
            crm_leads_total=await self.admin_repository.get_leads_total(),
            crm_new_leads=await self.admin_repository.get_new_leads_total(),
        )

    async def set_admin_role(
        self, request_user_id: int, target_user_id: int, is_admin: bool
    ) -> UserProfileSchema:
        await self._validate_admin(request_user_id)
        user = await self.admin_repository.set_user_admin_flag(
            user_id=target_user_id, is_admin=is_admin
        )
        if user is None:
            raise UserNotFoundException
        return UserProfileSchema.model_validate(user)

    async def _validate_admin(self, user_id: int) -> None:
        user = await self.user_repository.read_user_by_id(user_id)
        if user is None or not user.admin:
            raise PermissionDeniedException
