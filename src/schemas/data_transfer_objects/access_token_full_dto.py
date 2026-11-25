
from datetime import datetime

from pydantic import Field

from src.schemas.common import MixinIdSchema


class AccessTokenFullDto(MixinIdSchema):
    """DTO access-токена."""

    user_id: int = Field(description='ID пользователя')
    refresh_id: int = Field(description='ID refresh-токена')
    expire_at: datetime = Field(description='Время истечения токена')
    created_at: datetime | None = Field(
        default=None,
        description='Время создания токена',
    )
