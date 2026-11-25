from typing import List, Optional

from src.interfaces.controllers import BaseControllerInterface
from src.repositories import PostRepository
from src.schemas.data_transfer_objects import PostFullDto


class PostController(BaseControllerInterface):

    def __init__(self, post_repository: PostRepository):
        self._post_repository = post_repository

    async def get_post_by_id(
        self,
        post_id: int,
    ) -> Optional[PostFullDto]:
        return await self._post_repository.get_post_by_id(
            post_id=post_id,
        )

    async def get_post_many(self) -> List[PostFullDto]:
        return await self._post_repository.get_post_many()

    async def create_post(self, post: PostFullDto) -> PostFullDto:
        return await self._post_repository.create_post(post=post)

    async def update_post(
        self,
        post_id: int,
        post: PostFullDto,
    ) -> Optional[PostFullDto]:
        return await self._post_repository.update_post(
            post_id=post_id,
            post=post,
        )

    async def delete_post(self, post_id: int) -> bool:
        return await self._post_repository.delete_post(
            post_id=post_id,
        )