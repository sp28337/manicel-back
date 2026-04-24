import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.crm.models import LeadStatus, LeadSource


class LeadCreateSchema(BaseModel):
    full_name: str = Field(min_length=2, max_length=128)
    phone: str = Field(min_length=5, max_length=32)
    email: str | None = None
    comment: str | None = None
    source: LeadSource = LeadSource.OTHER


class LeadUpdateSchema(BaseModel):
    status: LeadStatus | None = None
    comment: str | None = None
    assigned_manager_id: int | None = None


class LeadSchema(BaseModel):
    id: int
    full_name: str
    phone: str
    email: str | None
    comment: str | None
    source: LeadSource
    status: LeadStatus
    assigned_manager_id: int | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
