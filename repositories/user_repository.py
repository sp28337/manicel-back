from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models.user_models import UserProfile


@dataclass
class UserRepository:

    db_session: Session

    def read_user(self, user_id: int) -> UserProfile | None:
        stmt = select(UserProfile).filter(UserProfile.id == user_id)
        with self.db_session as session:
            user = session.execute(stmt).scalar()
        return user

    def create_user(self, username: str, password: str, access_token: str) -> UserProfile:
        stmt = insert(UserProfile).values(
            username=username,
            password=password,
            access_token=access_token
        ).returning(UserProfile.id)

        with self.db_session as session:
            user_id = session.execute(stmt).scalar_one_or_none()
            session.commit()
            session.flush()
            return self.read_user(user_id)
