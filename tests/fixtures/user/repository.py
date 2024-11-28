import pytest

from dataclasses import dataclass

from app.user.schemas import UserCreateSchema
from tests.fixtures.user.models import UserProfileFactory


@dataclass
class FakeUserRepository:

    async def read_user_by_email(self, email: str) -> None:
        return None

    async def read_user_by_username(self, username: str) -> None:
        return None

    async def create_user(self, user_data: UserCreateSchema):
        return UserProfileFactory(username=user_data.username)


@pytest.fixture
def fake_user_repository() -> FakeUserRepository:
    return FakeUserRepository()
