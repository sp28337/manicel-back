import pytest
from app.settings import Settings
from app.user.auth.service import AuthService


pytestmark = pytest.mark.asyncio


async def test_get_google_redirect_url__success(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url
    google_redirect_url = auth_service.get_google_redirect_url()
    assert settings_google_redirect_url == google_redirect_url


async def test_get_yandex_redirect_url__success(auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url
    yandex_redirect_url = auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url == yandex_redirect_url


async def test_get_google_redirect_url__fail(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = "https://oauth.google.ru/"
    google_redirect_url = auth_service.get_google_redirect_url()
    assert settings_google_redirect_url != google_redirect_url


async def test_get_yandex_redirect_url__fail(auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = "https://oauth.yandex.ru/"
    yandex_redirect_url = auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url != yandex_redirect_url
