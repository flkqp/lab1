from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class MixinAutoIdModel:
    """Миксин для автоматического ID."""

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
        comment='Идентификатор',
        sort_order=-100,
    )