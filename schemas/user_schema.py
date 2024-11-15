from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserLoginSchema(BaseModel):
    id: int
    access_token: str


class UserSchema(UserCreateSchema):
    pass
