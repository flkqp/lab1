from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Integer, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column


class MixinSoftDeleteModel:
    """Миксин для мягкого удаления."""

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text('false'),
        comment='Удалено',
        sort_order=100,
    )

    deleted_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        comment='Удалил',
        sort_order=101,
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
        comment='Время удаления',
        sort_order=102,
    )