from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)
