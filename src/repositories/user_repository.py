
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel
from src.schemas.data_transfer_objects import UserFullDto
from .base_db_repository import BaseDbRepository


class UserRepository(
    BaseDbRepository[UserModel, UserFullDto, UserFullDto]
):
    """Репозиторий для работы с пользователями."""

    def __init__(self, async_db_session: AsyncSession):
        super().__init__(
            async_db_session=async_db_session,
            model_type=UserModel,
            full_schema_type=UserFullDto,
            short_schema_type=UserFullDto,
        )

    async def get_user_by_login(self, login: str):
        """Получает пользователя по логину."""
        statement = select(UserModel).where(
            UserModel.login == login,
            UserModel.is_deleted.is_(False),
        )

        result = await self._async_db_session.scalars(statement)
        return result.first()
