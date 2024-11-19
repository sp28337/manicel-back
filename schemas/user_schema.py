from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserSchema):
    email: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserGoogleCreateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str
    name: str | None = None
    google_access_token: str
