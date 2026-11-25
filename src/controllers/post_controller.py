
from src.repositories import PostRepository
from src.schemas.data_transfer_objects import PostFullDto


class PostController:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def get_post_by_id(self, post_id: int):
        return await self.repository.get_one_full_by_id(post_id)

    async def get_post_many(self):
        return await self.repository.get_all()

    async def create_post(self, post: PostFullDto):
        post.id = None
        return await self.repository.upsert(post)

    async def update_post(self, post_id: int, post: PostFullDto):
        post.id = post_id
        return await self.repository.upsert(post)

    async def delete_post(self, post_id: int):
        return await self.repository.delete_one_by_id(post_id)
