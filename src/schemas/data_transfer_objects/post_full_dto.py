from datetime import datetime
from typing import Optional

from pydantic import Field
from src.schemas.common import MixinIdSchema, MixinSoftDeleteSchema


class PostFullDto(MixinIdSchema, MixinSoftDeleteSchema):
    """Полный DTO поста."""

    name: str = Field(description='Название поста', examples=['My first post'])
    content: str = Field(description='Содержание поста', examples=['Post content'])
    created_at: Optional[datetime] = None