from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None]
    password: Mapped[str | None]
    name: Mapped[str | None]
    email: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)
    google_access_token: Mapped[str | None]
    yandex_access_token: Mapped[str | None]
