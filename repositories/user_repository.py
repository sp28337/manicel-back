from dataclasses import dataclass

from sqlalchemy import insert, select, update, delete

from infrastructure.database import LocalSession
from models.user_models import UserProfile
from schemas import UserCreateSchema, UserOAuthCreateSchema


@dataclass
class UserRepository:

    db_session: LocalSession

    def read_user_by_id(self, user_id: int) -> UserProfile | None:
        # stmt = select(UserProfile).filter(UserProfile.id == user_id)
        with self.db_session() as session:
            # user = session.execute(stmt).scalar()
            return session.get(UserProfile, user_id)

    def read_user_by_username(self, username: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.username == username)
        
        with self.db_session() as session:
            user = session.execute(stmt).scalar_one_or_none()
            return user

    def read_user_by_email(self, email: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.email == email)

        with self.db_session() as session:
            return session.execute(stmt).scalar_one_or_none()

    def read_user_by_yandex_access_token(self, access_token: str) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.yandex_access_token == access_token)

        with self.db_session() as session:
            return session.execute(stmt).scalar_one_or_none()

    def create_user(self, user_data: UserCreateSchema | UserOAuthCreateSchema) -> UserProfile:
        stmt = insert(UserProfile).values(
            user_data.model_dump(exclude_none=True)
        ).returning(UserProfile.id)

        with self.db_session() as session:
            user_id = session.execute(stmt).scalar()
            session.commit()
            session.flush()
            return self.read_user_by_id(user_id)

    def update_username(self, user_id: int, new_username: str) -> UserProfile:
        stmt = update(UserProfile
                      ).where(UserProfile.id == user_id
                              ).values(username=new_username
                                       ).returning(UserProfile.id)
        with self.db_session() as session:
            session.execute(stmt)
            session.commit()
            session.flush()
            return self.read_user_by_id(user_id)

    def update_name(self, user_id: int, new_name: str) -> UserProfile:
        stmt = update(UserProfile
                      ).where(UserProfile.id == user_id
                              ).values(name=new_name
                                       ).returning(UserProfile.id)
        with self.db_session() as session:
            session.execute(stmt)
            session.commit()
            session.flush()
            return self.read_user_by_id(user_id)

    def update_password(self, user_id: int, new_password: str) -> UserProfile:
        stmt = update(UserProfile
                      ).where(UserProfile.id == user_id
                              ).values(password=new_password
                                       ).returning(UserProfile.id)
        with self.db_session() as session:
            session.execute(stmt)
            session.commit()
            session.flush()
            return self.read_user_by_id(user_id)

    def delete_user(self, user_id: int) -> None:
        stmt = delete(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            session.execute(stmt)
            session.commit()
            session.flush()