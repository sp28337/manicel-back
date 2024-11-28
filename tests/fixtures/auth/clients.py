import pytest

from dataclasses import dataclass
from faker import Factory as FakerFactory

from app.settings import Settings
from app.user.auth.schemas import GoogleUserData, YandexUserData

faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> dict:
        google_access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token {code}"


@dataclass
class FakeYandexClient:
    settings: Settings

    async def get_user_info(self, code: str) -> dict:
        yandex_access_token = await self._get_user_access_token(code=code)
        return yandex_user_info_data()

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client() -> FakeGoogleClient:
    return FakeGoogleClient(settings=Settings())


@pytest.fixture
def yandex_client() -> FakeYandexClient:
    return FakeYandexClient(settings=Settings())


def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=faker.random_int(),
        email=faker.email(),
        verified_email=True,
        name=faker.name(),
        google_access_token=faker.sha256(),
    )


def yandex_user_info_data() -> YandexUserData:
    return YandexUserData(
        id=faker.random_int(),
        login=faker.name(),
        real_name=faker.name(),
        default_email=faker.email(),
        yandex_access_token=faker.sha256(),
    )
