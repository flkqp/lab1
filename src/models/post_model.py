from datetime import datetime

from sqlalchemy import String, Text, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

from settings import app_settings
from .base import Base
from .mixin_auto_id_model import MixinAutoIdModel
from .mixin_soft_delete_model import MixinSoftDeleteModel


class PostModel(Base, MixinAutoIdModel, MixinSoftDeleteModel):
    """Модель поста."""

    __tablename__ = 'post'
    __table_args__ = {'schema': app_settings.POSTS_SQL_SCHEMA}

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Название поста',
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment='Контент',
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('NOW()'),
        comment='Создан',
    )