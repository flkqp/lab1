
from pydantic import BaseModel, Field


class VerifyAccessTokenRequestDto(BaseModel):
    """DTO запроса на проверку access-токена."""

    access_token: str = Field(
        min_length=1,
        pattern=r'^[\w-]+\.[\w-]+\.[\w-]+$',
        description='Access-токен',
    )
