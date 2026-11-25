from typing import Annotated, List

from fastapi import Depends

from src.repositories import PostRepository
from src.schemas.data_transfer_objects import PostFullDto

from .common_dependencies import get_posts


async def get_post_repository(
    posts: Annotated[List[PostFullDto], Depends(get_posts)],
) -> PostRepository:
    return PostRepository(posts=posts)