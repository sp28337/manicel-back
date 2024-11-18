from dataclasses import dataclass

from sqlalchemy import insert, select

from infrastructure.database import LocalSession
from models.user_models import UserProfile


@dataclass
class UserRepository:

    db_session: LocalSession

    def read_user_by_id(self, user_id: int) -> UserProfile | None:
        stmt = select(UserProfile).filter(UserProfile.id == user_id)
        with self.db_session() as session:
            user = session.execute(stmt).scalar()
            return user

    def read_user_by_username(self, username: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            user = session.execute(stmt).scalar_one_or_none()
            return user

    def create_user(self, username: str, password: str) -> UserProfile:
        stmt = insert(UserProfile).values(
            username=username,
            password=password,
        ).returning(UserProfile.id)

        with self.db_session() as session:
            user_id = session.execute(stmt).scalar_one_or_none()
            session.commit()
            session.flush()
            return self.read_user_by_id(user_id)
