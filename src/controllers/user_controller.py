
from src.repositories import UserRepository
from src.schemas.data_transfer_objects import UserFullDto
from src.utils.common_utils import CommonUtils


class UserController:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_one_full_by_id(user_id)

    async def get_user_many(self):
        return await self.repository.get_all()

    async def create_user(self, user: UserFullDto):
        user.id = None
        user.password = CommonUtils.hash_password(user.password)
        return await self.repository.upsert(user)

    async def update_user(self, user_id: int, user: UserFullDto):
        user.id = user_id
        user.password = CommonUtils.hash_password(user.password)
        return await self.repository.upsert(user)

    async def delete_user(self, user_id: int):
        return await self.repository.delete_one_by_id(user_id)
