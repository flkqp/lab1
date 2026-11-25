
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AccessTokenModel


class AccessTokenRepository:
    """Репозиторий для работы с access-токенами."""

    def __init__(self, async_db_session: AsyncSession):
        self._async_db_session = async_db_session

    async def create(
        self,
        user_id: int,
        refresh_id: int,
        expire_at: datetime,
    ) -> AccessTokenModel:
        token = AccessTokenModel(
            user_id=user_id,
            refresh_id=refresh_id,
            expire_at=expire_at,
        )
        self._async_db_session.add(token)
        await self._async_db_session.flush()
        await self._async_db_session.refresh(token)
        return token

    async def get_by_id(self, token_id: int):
        statement = select(AccessTokenModel).where(
            AccessTokenModel.id == token_id,
            AccessTokenModel.expire_at > datetime.now(timezone.utc),
        )
        result = await self._async_db_session.scalars(statement)
        return result.first()

    async def delete_by_id(self, token_id: int) -> None:
        statement = delete(AccessTokenModel).where(
            AccessTokenModel.id == token_id
        )
        await self._async_db_session.execute(statement)

