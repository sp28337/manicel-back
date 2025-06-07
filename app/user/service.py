from dataclasses import dataclass

from app.exceptions import (
    UserNameAlreadyExistsException,
    UserEmailAlreadyExistsException,
    UserIncorrectPasswordException,
    UserNotFoundException,
)
from app.user.schemas import (
    UserCreateSchema,
    UserProfileSchema,
    UserUpdatePasswordSchema,
    ReadUserProfileSchema,
    UserUpdateNameSchema,
)
from app.user.auth.schemas import UserLoginSchema
from app.user.repository import UserRepository
from app.user.auth.service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def read_user_profile(self, user_id: int) -> ReadUserProfileSchema:
        return await self.user_repository.read_user_by_id(user_id=user_id)

    async def create_user(
        self, username: str, password: str, email: str
    ) -> UserLoginSchema:
        user_create_schema = UserCreateSchema(
            username=username, password=password, email=email
        )

        await self._check_user_exists(user_create_schema)

        new_user = await self.user_repository.create_user(user_create_schema)
        generated_access_token = self.auth_service.generate_access_token(
            user_id=new_user.id
        )
        return UserLoginSchema(user_id=new_user.id, access_token=generated_access_token)

    async def _check_user_exists(self, user: UserCreateSchema) -> None:
        if await self.user_repository.read_user_by_username(username=user.username):
            raise UserNameAlreadyExistsException

        if await self.user_repository.read_user_by_email(email=user.email):
            raise UserEmailAlreadyExistsException

    async def update_username(
        self, user_id: int, new_username: str
    ) -> UserProfileSchema:
        if await self.user_repository.read_user_by_username(username=new_username):
            raise UserNameAlreadyExistsException

        updated_user_profile = await self.user_repository.update_username(
            user_id=user_id, new_username=new_username
        )
        return UserProfileSchema.model_validate(updated_user_profile)

    async def update_name(self, user_id: int, body: UserUpdateNameSchema) -> UserProfileSchema:
        updated_user_profile = await self.user_repository.update_name(
            user_id=user_id, new_name=body.name
        )
        return UserProfileSchema.model_validate(updated_user_profile)

    async def update_password(
        self, user_id: int, body: UserUpdatePasswordSchema
    ) -> UserProfileSchema:
        user = await self.user_repository.read_user_by_id(user_id=user_id)
        if body.old_password != user.password:
            raise UserIncorrectPasswordException

        updated_user_profile = await self.user_repository.update_password(
            user_id=user_id, new_password=body.new_password
        )
        return UserProfileSchema.model_validate(updated_user_profile)

    async def delete_user(self, user_id: int):
        user = await self.read_user_profile(user_id=user_id)
        if not user:
            raise UserNotFoundException
        await self.user_repository.delete_user(user_id=user_id)
