import pytest_asyncio

from app.settings import Settings
from app.user.auth.clients import MailClient
from app.user.auth.service import AuthService
from app.user.repository import UserRepository


@pytest_asyncio.fixture
def mock_auth_service(yandex_client, google_client, fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(),
    )


@pytest_asyncio.fixture
def auth_service(yandex_client, google_client, mock_auth_service, get_db_session):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(),
    )
