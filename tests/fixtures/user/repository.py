import pytest

from dataclasses import dataclass


@dataclass
class FakeUserRepository:
    ...


@pytest.fixture
def user_repository() -> FakeUserRepository:
    return FakeUserRepository()
