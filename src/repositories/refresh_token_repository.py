
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import RefreshTokenModel


class RefreshTokenRepository:
    """Репозиторий для работы с refresh-токенами."""

    def __init__(self, async_db_session: AsyncSession):
        self._async_db_session = async_db_session

    async def create(
        self,
        user_id: int,
        expire_at: datetime,
    ) -> RefreshTokenModel:
        token = RefreshTokenModel(
            user_id=user_id,
            expire_at=expire_at,
        )
        self._async_db_session.add(token)
        await self._async_db_session.flush()
        await self._async_db_session.refresh(token)
        return token

    async def get_by_id(self, token_id: int):
        statement = select(RefreshTokenModel).where(
            RefreshTokenModel.id == token_id,
            RefreshTokenModel.expire_at > datetime.now(timezone.utc),
        )
        result = await self._async_db_session.scalars(statement)
        return result.first()

    async def delete_by_id(self, token_id: int) -> None:
        statement = delete(RefreshTokenModel).where(
            RefreshTokenModel.id == token_id
        )
        await self._async_db_session.execute(statement)

    async def delete_expired_tokens(self) -> int:
        statement = delete(RefreshTokenModel).where(
            RefreshTokenModel.expire_at <= datetime.now(timezone.utc)
        )
        result = await self._async_db_session.execute(statement)
        return result.rowcount or 0
