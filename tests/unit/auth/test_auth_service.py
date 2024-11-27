import pytest
import datetime as dt
from app.settings import Settings
from app.user.auth.service import AuthService
from jose import jwt

pytestmark = pytest.mark.asyncio


async def test_get_google_redirect_url__success(auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url
    google_redirect_url = auth_service.get_google_redirect_url()
    assert settings_google_redirect_url == google_redirect_url


async def test_get_yandex_redirect_url__success(auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url
    yandex_redirect_url = auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url == yandex_redirect_url


async def test_get_google_redirect_url__fail(auth_service: AuthService):
    settings_google_redirect_url = "https://oauth.google.ru/"
    google_redirect_url = auth_service.get_google_redirect_url()
    assert settings_google_redirect_url != google_redirect_url


async def test_get_yandex_redirect_url__fail(auth_service: AuthService):
    settings_yandex_redirect_url = "https://oauth.yandex.ru/"
    yandex_redirect_url = auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url != yandex_redirect_url


async def test_generate_access_token__success(auth_service: AuthService, settings: Settings):
    user_id = 7
    access_token = auth_service.generate_access_token(user_id)
    decoded_access_token = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALHORITHM])
    decoded_user_id = decoded_access_token.get("user_id")
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get("expire"), tz=dt.timezone.utc)
    assert user_id == decoded_user_id
    assert decoded_token_expire - dt.datetime.now(tz=dt.UTC) > dt.timedelta(days=6)


async def test_user_id_from_access_token__success(auth_service: AuthService):
    user_id = 18
    access_token = auth_service.generate_access_token(user_id)
    decoded_user_id = auth_service.get_user_id_from_access_token(access_token)
    assert user_id == decoded_user_id
