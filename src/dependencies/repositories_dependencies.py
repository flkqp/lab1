
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.common_dependencies import (
    sqlalchemy_async_session_generator,
)
from src.repositories import PostRepository, UserRepository
from src.repositories.access_token_repository import AccessTokenRepository
from src.repositories.refresh_token_repository import RefreshTokenRepository


async def get_post_repository(
    session: AsyncSession = Depends(sqlalchemy_async_session_generator),
) -> PostRepository:
    return PostRepository(async_db_session=session)


async def get_user_repository(
    session: AsyncSession = Depends(sqlalchemy_async_session_generator),
) -> UserRepository:
    return UserRepository(async_db_session=session)


async def get_access_token_repository(
    session: AsyncSession = Depends(sqlalchemy_async_session_generator),
) -> AccessTokenRepository:
    return AccessTokenRepository(async_db_session=session)


async def get_refresh_token_repository(
    session: AsyncSession = Depends(sqlalchemy_async_session_generator),
) -> RefreshTokenRepository:
    return RefreshTokenRepository(async_db_session=session)
