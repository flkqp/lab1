from pydantic import BaseModel, Field


class VerifyAccessTokenResponseDto(BaseModel):
    """DTO ответа при проверке access-токена."""

    access_token: str = Field(description='Проверенный access-токен')