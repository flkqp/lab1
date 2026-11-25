from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.controllers import PostController
from src.dependencies import get_post_controller
from src.schemas.data_transfer_objects import PostFullDto


post_router = APIRouter(
    prefix='/post',
    tags=['Посты'],
    deprecated=False,
    dependencies=None,
)


@post_router.get(
    '/many',
    response_model=List[PostFullDto],
    summary='Получить все посты',
    description='Возвращает список всех публикаций.',
)
async def get_post_many(
    post_controller: Annotated[
        PostController,
        Depends(get_post_controller),
    ],
) -> List[PostFullDto]:
    return await post_controller.get_post_many()


@post_router.get(
    '/{post_id}',
    response_model=PostFullDto,
    summary='Получить пост по ID',
)
async def get_post_by_id(
    post_controller: Annotated[
        PostController,
        Depends(get_post_controller),
    ],
    post_id: int = Path(
        description='ID поста',
        ge=1,
        examples=[1],
    ),
) -> PostFullDto:
    post = await post_controller.get_post_by_id(post_id=post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    return post


@post_router.post(
    '',
    response_model=PostFullDto,
    status_code=status.HTTP_201_CREATED,
    summary='Создать пост',
    description='Создаёт новую публикацию.',
)
async def create_post(
    post: PostFullDto,
    post_controller: Annotated[
        PostController,
        Depends(get_post_controller),
    ],
) -> PostFullDto:
    return await post_controller.create_post(post=post)


@post_router.put(
    '/{post_id}',
    response_model=PostFullDto,
    summary='Редактировать пост',
)
async def update_post(
    post: PostFullDto,
    post_controller: Annotated[
        PostController,
        Depends(get_post_controller),
    ],
    post_id: int = Path(description='ID поста', ge=1),
) -> PostFullDto:
    updated_post = await post_controller.update_post(
        post_id=post_id,
        post=post,
    )

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )

    return updated_post


@post_router.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить пост',
)
async def delete_post(
    post_controller: Annotated[
        PostController,
        Depends(get_post_controller),
    ],
    post_id: int = Path(description='ID поста', ge=1),
):
    deleted = await post_controller.delete_post(post_id=post_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found',
        )