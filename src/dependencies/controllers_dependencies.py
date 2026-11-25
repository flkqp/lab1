from typing import Annotated

from fastapi import Depends

from src.controllers import PostController, UserController
from src.repositories import PostRepository, UserRepository
from .repositories_dependencies import (
    get_post_repository,
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