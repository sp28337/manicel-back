import datetime
import enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.orm_base import Base
from app.user.models import UserProfile


class LeadStatus(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class LeadSource(enum.Enum):
    WEBSITE = "website"
    INSTAGRAM = "instagram"
    TELEGRAM = "telegram"
    REFERRAL = "referral"
    OTHER = "other"


class Lead(Base):
    __tablename__ = "crm_leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str | None]
    comment: Mapped[str | None]
    source: Mapped[LeadSource] = mapped_column(default=LeadSource.OTHER)
    status: Mapped[LeadStatus] = mapped_column(default=LeadStatus.NEW)
    assigned_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("user_profiles.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=func.CURRENT_TIMESTAMP()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
    )

    assigned_manager: Mapped[UserProfile | None] = relationship(lazy="joined")
