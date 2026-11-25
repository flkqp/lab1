from typing import Annotated

from fastapi import Depends

from src.controllers import PostController
from src.repositories import PostRepository

from .repositories_dependencies import get_post_repository


async def get_post_controller(
    post_repository: Annotated[
        PostRepository,
        Depends(get_post_repository),
    ],
) -> PostController:
    return PostController(post_repository=post_repository)