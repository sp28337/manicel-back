from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseModel):
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    PROD_URL: str = ""
    DEV_URL: str = ""
    FRONT_URL: str = ""


class Settings(BaseSettings):
    ENV: str = "dev"

    DB_HOST: str = ""
    DB_PORT: int = 7777
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_DRIVER: str = ""
    DB_NAME: str = ""

    JWT_SECRET_KEY: str = ""
    JWT_ENCODE_ALHORITHM: str = "HS256"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_SECRET_KEY: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    YANDEX_CLIENT_ID: str = ""
    YANDEX_SECRET_KEY: str = ""
    YANDEX_REDIRECT_URI: str = ""
    YANDEX_TOKEN_URI: str = "https://oauth.yandex.ru/token"

    CALLBACK_REDIRECT_URI: str = ""
    COOKIES_DOMAIN: str = ""

    GUNICORN_BIND: str = ""
    GUNICORN_WORKERS: int = 1

    CORS: CORSSettings = CORSSettings()

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        # extra="ignore",
    )

    @property
    def get_db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self):
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email%20&access_type=offline"

    @property
    def yandex_redirect_url(self):
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
