import pytest

from dataclasses import dataclass

from app.settings import Settings


@dataclass
class FakeGoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> dict:
        google_access_token = await self._get_user_access_token(code=code)
        return {"fake_access_token": google_access_token}

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token {code}"


@dataclass
class FakeYandexClient:
    settings: Settings

    async def get_user_info(self, code: str) -> dict:
        yandex_access_token = await self._get_user_access_token(code=code)
        return {"fake_access_token": yandex_access_token}

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client() -> FakeGoogleClient:
    return FakeGoogleClient(settings=Settings())


@pytest.fixture
def yandex_client() -> FakeYandexClient:
    return FakeYandexClient(settings=Settings())
