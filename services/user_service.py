from dataclasses import dataclass

from exceptions import UserNameAlreadyExistsException, UserEmailAlreadyExistsException
from schemas import UserLoginSchema, UserCreateSchema
from repositories import UserRepository
from services.auth_service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str, email: str) -> UserLoginSchema:
        user_create_schema = UserCreateSchema(
                username=username,
                password=password,
                email=email
            )

        self._check_user_exists(user_create_schema)

        new_user = self.user_repository.create_user(user_create_schema)
        generated_access_token = self.auth_service.generate_access_token(user_id=new_user.id, is_admin=new_user.admin)
        return UserLoginSchema(
            user_id=new_user.id,
            access_token=generated_access_token
        )

    def _check_user_exists(self, user: UserCreateSchema) -> None:
        if self.user_repository.read_user_by_username(username=user.username):
            raise UserNameAlreadyExistsException

        if self.user_repository.read_user_by_email(email=user.email):
            raise UserEmailAlreadyExistsException
