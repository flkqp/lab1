
from typing import Annotated

from fastapi import Depends

from src.controllers import AuthController, PostController, UserController
from src.repositories import (
    AccessTokenRepository,
    PostRepository,
    RefreshTokenRepository,
    UserRepository,
)
from .repositories_dependencies import (
    get_access_token_repository,
    get_post_repository,
    get_refresh_token_repository,
    get_user_repository,
)


async def get_post_controller(
    repository: Annotated[PostRepository, Depends(get_post_repository)],
) -> PostController:
    return PostController(repository)


async def get_user_controller(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserController:
    return UserController(repository)


async def get_auth_controller(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    access_token_repository: Annotated[
        AccessTokenRepository,
        Depends(get_access_token_repository),
    ],
    refresh_token_repository: Annotated[
        RefreshTokenRepository,
        Depends(get_refresh_token_repository),
    ],
) -> AuthController:
    return AuthController(
        user_repository=user_repository,
        access_token_repository=access_token_repository,
        refresh_token_repository=refresh_token_repository,
    )
