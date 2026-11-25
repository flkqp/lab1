
from pydantic import BaseModel, Field


class TokenDto(BaseModel):
    """DTO для передачи JWT-токенов."""

    access_token: str = Field(description='Access-токен')
    refresh_token: str = Field(description='Refresh-токен')
    token_type: str = Field(default='bearer', description='Тип токена')
