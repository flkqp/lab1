from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.repositories import BaseRepositoryInterface
from src.models import MixinAutoIdModel
from src.schemas.common import BaseSchema

ModelType = TypeVar('ModelType', bound=MixinAutoIdModel)
FullSchema = TypeVar('FullSchema', bound=BaseSchema)
ShortSchema = TypeVar('ShortSchema', bound=BaseSchema)


class BaseDbRepository(
    BaseRepositoryInterface,
    Generic[ModelType, FullSchema, ShortSchema],


):
    """Базовый репозиторий для работы с БД."""
    async def get_all(self):
        statement = select(self._model_type).where(
            self._model_type.is_deleted.is_(False)
        )
        result = await self._async_db_session.scalars(statement)
        return [
            self._full_schema_type.model_validate(item)
            for item in result.all()
        ]

    def __init__(
        self,
        async_db_session: AsyncSession,
        model_type: Type[ModelType],
        full_schema_type: Type[FullSchema],
        short_schema_type: Type[ShortSchema],
    ):
        self._async_db_session = async_db_session
        self._model_type = model_type
        self._full_schema_type = full_schema_type
        self._short_schema_type = short_schema_type

    @property
    def async_db_session(self) -> AsyncSession:
        return self._async_db_session

    @property
    def model_type(self) -> Type[ModelType]:
        return self._model_type

    @property
    def short_schema_type(self) -> Type[ShortSchema]:
        return self._short_schema_type

    @property
    def full_schema_type(self) -> Type[FullSchema]:
        return self._full_schema_type

    async def commit(self) -> None:
        await self._async_db_session.commit()

    async def get_one_full_by_id(
        self,
        object_id: int,
    ) -> Optional[FullSchema]:
        model = await self._async_db_session.get(
            self._model_type,
            object_id,
        )

        if model is None or getattr(model, 'is_deleted', False):
            return None

        return self._full_schema_type.model_validate(model)

    async def upsert(self, dto: FullSchema) -> FullSchema:
        """
        Создание или обновление объекта по ID.
        Если ID отсутствует — создаётся новая запись.
        Если ID существует — запись обновляется.
        """

        data = dto.model_dump(
            exclude={'id', 'created_at'},
            exclude_unset=True,
        )

        object_id = getattr(dto, 'id', None)

        if object_id is not None:
            model = await self._async_db_session.get(
                self._model_type,
                object_id,
            )
        else:
            model = None

        if model is None:
            model = self._model_type(**data)
            self._async_db_session.add(model)
        else:
            if getattr(model, 'is_deleted', False):
                raise ValueError('Нельзя обновить удалённую запись')

            for field, value in data.items():
                if hasattr(model, field):
                    setattr(model, field, value)

        await self._async_db_session.flush()
        await self._async_db_session.refresh(model)

        return self._full_schema_type.model_validate(model)

    async def delete_one_by_id(self, object_id: int) -> bool:
        """Физическое удаление записи по ID."""

        delete_statement = delete(self._model_type).where(
            self._model_type.id == object_id
        )

        result = await self._async_db_session.execute(
            statement=delete_statement
        )

        return result.rowcount == 1