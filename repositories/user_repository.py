from dataclasses import dataclass

from sqlalchemy import insert, select, update, delete, Select, Insert, Update, Delete

from infrastructure.database import LocalAsyncSession
from models.user_models import UserProfile
from schemas import UserCreateSchema, UserOAuthCreateSchema


@dataclass
class UserRepository:

    db_session: LocalAsyncSession

    async def read_user_by_id(self, user_id: int) -> UserProfile | None:
        # stmt = select(UserProfile).filter(UserProfile.id == user_id)
        async with self.db_session() as session:
            # user = session.execute(stmt).scalar()
            return await session.get(UserProfile, user_id)

    async def read_user_by_username(self, username: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.username == username)

        async with self.db_session() as session:
            user = (await session.execute(stmt)).scalar_one_or_none()
            return user

    async def read_user_by_email(self, email: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.email == email)

        async with self.db_session() as session:
            return (await session.execute(stmt)).scalar_one_or_none()

    async def read_user_by_yandex_access_token(
        self, access_token: str
    ) -> UserProfile | None:
        stmt = select(UserProfile).where(
            UserProfile.yandex_access_token == access_token
        )

        async with self.db_session() as session:
            return (await session.execute(stmt)).scalar_one_or_none()

    async def create_user(
        self, user_data: UserCreateSchema | UserOAuthCreateSchema
    ) -> UserProfile:
        stmt = (
            insert(UserProfile)
            .values(user_data.model_dump(exclude_none=True))
            .returning(UserProfile.id)
        )

        async with self.db_session() as session:
            user_id = (await session.execute(stmt)).scalar()
            await session.commit()
            await session.flush()
            return await self.read_user_by_id(user_id)

    async def update_username(self, user_id: int, new_username: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(username=new_username)
            .returning(UserProfile.id)
        )
        async with self.db_session() as session:
            await self._execute_commit_flush(s=session, query=stmt)
            return await self.read_user_by_id(user_id)

    async def update_name(self, user_id: int, new_name: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(name=new_name)
            .returning(UserProfile.id)
        )
        async with self.db_session() as session:
            await self._execute_commit_flush(s=session, query=stmt)
            return await self.read_user_by_id(user_id)

    async def update_password(self, user_id: int, new_password: str) -> UserProfile:
        stmt = (
            update(UserProfile)
            .where(UserProfile.id == user_id)
            .values(password=new_password)
            .returning(UserProfile.id)
        )
        async with self.db_session() as session:
            await self._execute_commit_flush(s=session, query=stmt)
            return await self.read_user_by_id(user_id)

    async def delete_user(self, user_id: int) -> None:
        stmt = delete(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session() as session:
            await self._execute_commit_flush(s=session, query=stmt)

    @staticmethod
    async def _execute_commit_flush(
        s: LocalAsyncSession, query: Select | Insert | Update | Delete
    ) -> None:
        await s.execute(query)
        await s.commit()
        await s.flush()
