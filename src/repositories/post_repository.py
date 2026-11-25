from typing import List, Optional

from src.interfaces.repositories import BaseRepositoryInterface
from src.schemas.data_transfer_objects import PostFullDto


class PostRepository(BaseRepositoryInterface):

    def __init__(self, posts: List[PostFullDto]):
        self._posts = posts

    async def get_post_by_id(
        self,
        post_id: int,
    ) -> Optional[PostFullDto]:
        for post in self._posts:
            if post.id == post_id:
                return post

        return None

    async def get_post_many(self) -> List[PostFullDto]:
        return self._posts

    async def create_post(
        self,
        post: PostFullDto,
    ) -> PostFullDto:
        new_id = max(
            (item.id for item in self._posts if item.id is not None),
            default=0,
        ) + 1

        new_post = PostFullDto(
            id=new_id,
            author_name=post.author_name,
            content=post.content,
        )

        self._posts.append(new_post)
        return new_post

    async def update_post(
        self,
        post_id: int,
        post: PostFullDto,
    ) -> Optional[PostFullDto]:
        for index, existing_post in enumerate(self._posts):
            if existing_post.id == post_id:
                updated_post = PostFullDto(
                    id=post_id,
                    author_name=post.author_name,
                    content=post.content,
                )
                self._posts[index] = updated_post
                return updated_post

        return None

    async def delete_post(self, post_id: int) -> bool:
        for index, post in enumerate(self._posts):
            if post.id == post_id:
                del self._posts[index]
                return True

        return False