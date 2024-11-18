from dataclasses import dataclass
import datetime as dt

from jose import jwt
from jose.exceptions import JWTError
from exceptions import UserNotFoundException, UserIncorrectPasswordException, TokenExpiredException, \
    IncorrectTokenException, PermissionDeniedException
from models import UserProfile
from repositories import UserRepository
from schemas import UserSchema, UserLoginSchema
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserSchema:
        user: UserProfile = self.user_repository.read_user_by_username(username)

        self._validate_auth_user(user, password)

        generated_access_token = self.generate_access_token(user_id=user.id, is_admin=user.admin)
        return UserLoginSchema(id=user.id, access_token=generated_access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserIncorrectPasswordException

    def generate_access_token(self, user_id: int, is_admin: bool) -> str:
        expires_date_unix = (dt.datetime.now(dt.UTC) + dt.timedelta(days=7)).timestamp()

        access_token: str = jwt.encode(
            claims={
                "user_id": user_id,
                "admin": is_admin,
                "expire": expires_date_unix
            },
            key=self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALHORITHM
        )

        return access_token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload: dict = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALHORITHM]
            )
        except JWTError:
            raise IncorrectTokenException

        if payload["expire"] < dt.datetime.now(dt.UTC).timestamp():
            raise TokenExpiredException

        return payload["user_id"]

    def check_is_user_admin_from_access_token(self, access_token: str) -> bool:
        try:
            payload: dict = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALHORITHM]
            )
        except JWTError:
            raise IncorrectTokenException

        if payload["admin"]:
            return True
        else:
            raise PermissionDeniedException
