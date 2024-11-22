from dataclasses import dataclass

from exceptions import UserNameAlreadyExistsException, UserEmailAlreadyExistsException, UserIncorrectPasswordException
from schemas import UserLoginSchema, UserCreateSchema, UserProfileSchema
from repositories import UserRepository
from services.auth_service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def read_user_profile(self, user_id: int) -> UserProfileSchema:
        return self.user_repository.read_user_by_id(user_id=user_id)

    def create_user(self, username: str, password: str, email: str) -> UserLoginSchema:
        user_create_schema = UserCreateSchema(
                username=username,
                password=password,
                email=email
            )

        self._check_user_exists(user_create_schema)

        new_user = self.user_repository.create_user(user_create_schema)
        generated_access_token = self.auth_service.generate_access_token(user_id=new_user.id)
        return UserLoginSchema(
            user_id=new_user.id,
            access_token=generated_access_token
        )

    def _check_user_exists(self, user: UserCreateSchema) -> None:
        if self.user_repository.read_user_by_username(username=user.username):
            raise UserNameAlreadyExistsException

        if self.user_repository.read_user_by_email(email=user.email):
            raise UserEmailAlreadyExistsException

    def update_username(self, user_id: int, new_username: str) -> UserProfileSchema:
        if self.user_repository.read_user_by_username(username=new_username):
            raise UserNameAlreadyExistsException

        updated_user_profile = self.user_repository.update_username(
            user_id=user_id,
            new_username=new_username
        )
        return UserProfileSchema.model_validate(updated_user_profile)

    def update_name(self, user_id: int, new_name: str) -> UserProfileSchema:
        updated_user_profile = self.user_repository.update_name(
            user_id=user_id,
            new_name=new_name
        )
        return UserProfileSchema.model_validate(updated_user_profile)

    def update_password(self, user_id: int, old_password: str | None, new_password: str) -> UserProfileSchema:
        user = self.user_repository.read_user_by_id(user_id=user_id)
        if old_password != user.password:
            raise UserIncorrectPasswordException

        updated_user_profile = self.user_repository.update_password(
            user_id=user_id,
            new_password=new_password
        )
        return UserProfileSchema.model_validate(updated_user_profile)
