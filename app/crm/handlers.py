from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.crm.models import LeadStatus
from app.crm.schemas import LeadCreateSchema, LeadSchema, LeadUpdateSchema
from app.crm.service import CRMService
from app.dependencies import get_crm_service, get_request_user_id
from app.exceptions import (
    LeadNotFoundException,
    PermissionDeniedException,
    UserNotFoundException,
)

router = APIRouter(prefix="/crm", tags=["crm"])


@router.post("/leads", response_model=LeadSchema, status_code=status.HTTP_201_CREATED)
async def create_lead(
    body: LeadCreateSchema,
    crm_service: Annotated[CRMService, Depends(get_crm_service)],
):
    return await crm_service.create_lead(body)


@router.get("/leads", response_model=list[LeadSchema])
async def get_leads(
    crm_service: Annotated[CRMService, Depends(get_crm_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
    status_filter: LeadStatus | None = None,
):
    try:
        return await crm_service.get_leads(user_id=user_id, status=status_filter)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)


@router.patch("/leads/{lead_id}", response_model=LeadSchema)
async def update_lead(
    lead_id: int,
    body: LeadUpdateSchema,
    crm_service: Annotated[CRMService, Depends(get_crm_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
):
    try:
        return await crm_service.update_lead(
            lead_id=lead_id, user_id=user_id, body=body
        )
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
    except (LeadNotFoundException, UserNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
