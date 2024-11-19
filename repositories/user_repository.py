from dataclasses import dataclass

from sqlalchemy import insert, select

from infrastructure.database import LocalSession
from models.user_models import UserProfile
from schemas import UserCreateSchema, UserGoogleCreateSchema


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

    def read_user_by_email(self, email: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.email == email)

        with self.db_session() as session:
            return session.execute(stmt).scalar_one_or_none()

    def read_user_by_access_token(self, access_token: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.google_access_token == access_token)

        with self.db_session() as session:
            return session.execute(stmt).scalar_one_or_none()

    def create_user(self, user_data: UserCreateSchema | UserGoogleCreateSchema) -> UserProfile:
        stmt = insert(UserProfile).values(
            user_data.model_dump(exclude_none=True)
        ).returning(UserProfile.id)

        with self.db_session() as session:
            user_id = session.execute(stmt).scalar()
            session.commit()
            session.flush()
            return self.read_user_by_id(user_id)
