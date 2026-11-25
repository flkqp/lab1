from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import PostRepository, UserRepository
from .common_dependencies import sqlalchemy_async_session_generator


async def get_post_repository(
    async_db_session: Annotated[
        AsyncSession,
        Depends(sqlalchemy_async_session_generator),
    ],
) -> PostRepository:
    return PostRepository(async_db_session=async_db_session)


async def get_user_repository(
    async_db_session: Annotated[
        AsyncSession,
        Depends(sqlalchemy_async_session_generator),
    ],
) -> UserRepository:
    return UserRepository(async_db_session=async_db_session)