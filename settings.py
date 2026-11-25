
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    SQL_DSN: str = 'postgresql+asyncpg://user:password@localhost:5432/db'

    USERS_SQL_SCHEMA: str = 'users'
    POSTS_SQL_SCHEMA: str = 'post'

    SECRET_KEY: str = 'change-this-secret-key-before-deployment'
    JWT_ALGORITHM: str = 'HS256'

    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRES_DAYS: int = 7


app_settings = AppSettings()
