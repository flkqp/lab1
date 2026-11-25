from typing import List

from src.schemas.data_transfer_objects import PostFullDto


posts = [
    PostFullDto(id=1, author_name='Bob', content='52'),
    PostFullDto(id=2, author_name='Billy', content='67'),
    PostFullDto(id=3, author_name='John', content='Lorem ipsum'),
]


async def get_posts() -> List[PostFullDto]:
    return posts