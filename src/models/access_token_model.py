
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from settings import app_settings
from .base import Base
from .mixin_auto_id_model import MixinAutoIdModel


class AccessTokenModel(Base, MixinAutoIdModel):
    """Модель access-токена."""

    __tablename__ = 'access_token'
    __table_args__ = {'schema': app_settings.USERS_SQL_SCHEMA}

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            f'{app_settings.USERS_SQL_SCHEMA}.user.id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )

    refresh_id: Mapped[int] = mapped_column(
        ForeignKey(
            f'{app_settings.USERS_SQL_SCHEMA}.refresh_token.id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )

    expire_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
