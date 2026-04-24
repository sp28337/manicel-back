from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.admin.schemas import DashboardSchema, SetAdminSchema
from app.admin.service import AdminService
from app.dependencies import get_admin_service, get_request_user_id
from app.exceptions import PermissionDeniedException, UserNotFoundException
from app.user.schemas import UserProfileSchema

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", response_model=DashboardSchema)
async def get_dashboard(
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
):
    try:
        return await admin_service.get_dashboard(user_id=user_id)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.patch("/users/{target_user_id}/admin", response_model=UserProfileSchema)
async def set_user_admin_flag(
    target_user_id: int,
    body: SetAdminSchema,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
):
    try:
        return await admin_service.set_admin_role(
            request_user_id=user_id,
            target_user_id=target_user_id,
            is_admin=body.is_admin,
        )
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
