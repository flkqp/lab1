from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Настройки приложения.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    SQL_DSN: str = 'postgresql+asyncpg://user:password@localhost:5432/db'
    USERS_SQL_SCHEMA: str = 'users'
    POSTS_SQL_SCHEMA: str = 'post'


app_settings = AppSettings()