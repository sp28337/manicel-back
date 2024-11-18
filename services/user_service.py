from dataclasses import dataclass

from exceptions import UserAlreadyExistsException
from schemas import UserLoginSchema
from repositories import UserRepository
from services.auth_service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:

        if self.user_repository.read_user_by_username(username=username):
            raise UserAlreadyExistsException

        new_user = self.user_repository.create_user(
            username=username,
            password=password,
        )
        generated_access_token = self.auth_service.generate_access_token(user_id=new_user.id, is_admin=new_user.admin)
        return UserLoginSchema(
            id=new_user.id,
            access_token=generated_access_token
        )

