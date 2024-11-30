import pytest
from sqlalchemy import select, insert

from app.user.models import UserProfile
from tests.fixtures.user.models import EXISTS_GOOGLE_USER_ID, EXISTS_GOOGLE_EMAIL


# pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio(loop_scope="session")
async def test_google_auth__login_exist_user(auth_service, get_db_session):
    code = "test_code"
    stmt = insert(UserProfile).values(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_EMAIL,
    )
    await get_db_session.execute(stmt)
    user_data = await auth_service.google_auth(code=code)

    stmt = select(UserProfile).where(UserProfile.id == user_data.user_id)
    login_user = (await get_db_session.execute(stmt)).scalar_one_or_none()

    assert login_user.email == EXISTS_GOOGLE_EMAIL
    assert user_data.user_id == EXISTS_GOOGLE_USER_ID


@pytest.mark.asyncio(loop_scope="session")
async def test_google_auth__login_not_exist_user(auth_service, get_db_session):
    code = "test_code"

    users = (await get_db_session.execute(select(UserProfile))).scalars().all()
    user = await auth_service.google_auth(code=code)

    assert len(users) == 0
    assert user is not None

    stmt = select(UserProfile).where(UserProfile.id == user.user_id)
    login_user = (await get_db_session.execute(stmt)).scalars().first()

    assert login_user is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_base_login__success(auth_service, get_db_session):
    username = "test_username"
    password = "test_password"
    email = "test_email"

    stmt = insert(UserProfile).values(
        username=username,
        password=password,
        email=email
    )
    await get_db_session.execute(stmt)
    await get_db_session.commit()
    await get_db_session.flush()
    stmt = select(UserProfile).where(UserProfile.username == username)
    login_user = (await get_db_session.execute(stmt)).scalars().first()

    user_data = await auth_service.login(username=username, password=password)

    assert login_user is not None
    assert user_data.user_id == login_user.id
