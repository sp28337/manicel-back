import string
from dataclasses import dataclass
from random import choice

from schemas import UserLoginSchema
from repositories import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        generated_access_token = self._generate_access_token(10)
        user = self.user_repository.create_user(
            username=username,
            password=password,
            access_token=generated_access_token
        )
        return UserLoginSchema(
            id=user.id,
            access_token=user.access_token
        )

    @staticmethod
    def _generate_access_token(n) -> str:
        return "".join(choice(string.ascii_uppercase + string.digits) for _ in range(n))
