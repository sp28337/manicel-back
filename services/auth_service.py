from dataclasses import dataclass

from exceptions import UserNotFoundException, UserIncorrectPasswordException
from models import UserProfile
from repositories import UserRepository
from schemas import UserSchema, UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserSchema:
        user: UserProfile = self.user_repository.read_user_by_username(username)

        self._validate_auth_user(user, password)

        return UserLoginSchema(id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserIncorrectPasswordException
