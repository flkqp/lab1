
from pydantic import BaseModel, Field


class RefreshTokenRequestDto(BaseModel):
    """DTO запроса на обновление или удаление refresh-токена."""

    refresh_token: str = Field(
        min_length=1,
        pattern=r'^[\w-]+\.[\w-]+\.[\w-]+$',
        description='Refresh-токен',
    )
