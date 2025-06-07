import datetime

from pydantic import BaseModel, model_validator, ConfigDict


class UserSchema(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserSchema):
    email: str


class ReadUserProfileSchema(BaseModel):
    id: int
    username: str | None
    password: str | None
    name: str | None
    email: str
    admin: bool
    created_at: datetime.datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserProfileSchema(ReadUserProfileSchema):
    google_access_token: str | None
    yandex_access_token: str | None


class UserUpdatePasswordSchema(BaseModel):
    old_password: str | None
    new_password: str
    repeat_new_password: str

    @model_validator(mode="after")
    def check_new_password_equal_repeat_new_password(self):
        if self.new_password != self.repeat_new_password:
            raise ValueError("Passwords do not match")
        return self


class UserUpdateNameSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdateUsernameSchema(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdateEmailSchema(BaseModel):
    email: str | None

    model_config = ConfigDict(from_attributes=True)
