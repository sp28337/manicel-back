import datetime

from pydantic import BaseModel, model_validator


class UserSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserSchema):
    email: str


class UserProfileSchema(BaseModel):
    id: int
    username: str | None
    password: str | None
    name: str | None
    email: str
    admin: bool
    google_access_token: str | None
    yandex_access_token: str | None
    created_at: datetime.datetime | None

    class Config:
        from_attributes = True


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


class UserUpdatePasswordSchema(BaseModel):
    old_password: str | None
    new_password: str
    repeat_new_password: str

    @model_validator(mode="after")
    def check_new_password_equal_repeat_new_password(self):
        if self.new_password != self.repeat_new_password:
            raise ValueError("Passwords do not match")
        return self
