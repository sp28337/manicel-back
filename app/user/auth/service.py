from dataclasses import dataclass
import datetime as dt

from jose import jwt
from jose.exceptions import JWTError

from app.user.auth.clients import GoogleClient, YandexClient
from app.exceptions import (
    TokenExpiredException,
    UserIncorrectPasswordException,
    UserNotFoundException,
    IncorrectTokenException,
)
from app.user.models import UserProfile
from app.user.repository import UserRepository
from app.user.auth.schemas import UserLoginSchema, UserOAuthCreateSchema
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def google_auth(self, code: str) -> UserLoginSchema:
        # -- Запрос в Google с полученным кодом
        user_data = await self.google_client.get_user_info(code=code)

        # -- Если юзер существует
        if user := await self.user_repository.read_user_by_email(email=user_data.email):
            # -- Генерируем токен доступа
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        else:  # -- Если юзера нет - создаем юзера
            create_user_data = UserOAuthCreateSchema(
                username=f"user_{user_data.id}",
                email=user_data.email,
                name=user_data.name,
                google_access_token=user_data.google_access_token,
            )
            # -- И записываем в базу данных
            created_user = await self.user_repository.create_user(create_user_data)
            # -- Генерируем токен доступа
            access_token = self.generate_access_token(user_id=created_user.id)
            return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.read_user_by_email(
            email=user_data.default_email
        ):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserOAuthCreateSchema(
            username=f"{user_data.login}_{user_data.id}",
            email=user_data.default_email,
            name=user_data.name,
            yandex_access_token=user_data.yandex_access_token,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user: UserProfile = await self.user_repository.read_user_by_username(
            username=username
        )
        self._validate_auth_user(user, password)

        access_token = self.generate_access_token(user_id=user.id, access=user.admin)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserIncorrectPasswordException

    def generate_access_token(self, user_id: int, access: bool = False) -> str:
        expires_date_unix = (dt.datetime.now(dt.UTC) + dt.timedelta(days=7)).timestamp()

        access_token: str = jwt.encode(
            claims={
                "user_id": user_id,
                "expire": expires_date_unix,
                "access": access,
            },
            key=self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALHORITHM,
        )
        return access_token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload: dict = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALHORITHM],
            )
        except JWTError:
            raise IncorrectTokenException

        if payload["expire"] < dt.datetime.now(dt.UTC).timestamp():
            raise TokenExpiredException

        return payload["user_id"]
