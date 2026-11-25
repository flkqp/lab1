
from datetime import datetime

from pydantic import Field

from src.schemas.common import MixinIdSchema


class RefreshTokenFullDto(MixinIdSchema):
    """DTO refresh-токена."""

    user_id: int = Field(description='ID пользователя')
    expire_at: datetime = Field(description='Время истечения токена')
    created_at: datetime | None = Field(
        default=None,
        description='Время создания токена',
    )
