from sqlalchemy import insert, select, update, delete, Select, Insert, Update, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import UserProfile
from app.user.schemas import UserCreateSchema
from app.user.auth.schemas import UserOAuthCreateSchema


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def read_user_by_id(self, user_id: int) -> UserProfile | None:
        # stmt = select(UserProfile).filter(UserProfile.id == user_id)
        # user = session.execute(stmt).scalar()
        return await self.db_session.get(UserProfile, user_id)

    async def read_user_by_username(self, username: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.username == username)
        result = await self.db_session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def read_user_by_email(self, email: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.email == email)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def read_user_by_yandex_access_token(
        self, access_token: str
    ) -> UserProfile | None:
        stmt = select(UserProfile).where(
            UserProfile.yandex_access_token == access_token
        )
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self, user_data: UserCreateSchema | UserOAuthCreateSchema
    ) -> UserProfile:
        stmt = (
            insert(UserProfile)
            .values(user_data.model_dump(exclude_none=True))
            .returning(UserProfile.id)
        )
        result = await self.db_session.execute(stmt)
        user_id = result.scalar()
        await self.db_session.commit()
        await self.db_session.flush()
        return await self.read_user_by_id(user_id)

    async def update_username(self, user_id: int, new_username: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(username=new_username)
            .returning(UserProfile.id)
        )
        await self._execute_commit_flush(s=self.db_session, query=stmt)
        return await self.read_user_by_id(user_id)

    async def update_name(self, user_id: int, new_name: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(name=new_name)
            .returning(UserProfile.id)
        )
        await self._execute_commit_flush(s=self.db_session, query=stmt)
        return await self.read_user_by_id(user_id)

    async def update_email(self, user_id: int, new_email: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(email=new_email)
            .returning(UserProfile.id)
        )
        await self._execute_commit_flush(s=self.db_session, query=stmt)
        return await self.read_user_by_id(user_id)

    async def update_password(self, user_id: int, new_password: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(password=new_password)
            .returning(UserProfile.id)
        )
        await self._execute_commit_flush(s=self.db_session, query=stmt)
        return await self.read_user_by_id(user_id)

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(UserProfile).where(UserProfile.id == user_id)
        await self._execute_commit_flush(s=self.db_session, query=stmt)

    @staticmethod
    async def _execute_commit_flush(
        s: AsyncSession, query: Select | Insert | Update | Delete
    ) -> None:
        await s.execute(query)
        await s.commit()
        await s.flush()
