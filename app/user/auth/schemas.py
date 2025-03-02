from pydantic import BaseModel, Field, model_validator


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    google_access_token: str


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias="real_name")
    default_email: str
    yandex_access_token: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserOAuthCreateSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    name: str | None = None
    google_access_token: str | None = None
    yandex_access_token: str | None = None

    @model_validator(mode="after")
    def check_google_or_yandex_access_token_is_not_none(self):
        if self.google_access_token is None and self.yandex_access_token is None:
            raise ValueError("google or yandex access token must be provided")
        return self
