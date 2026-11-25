from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.controllers import PostController
from src.dependencies.controllers_dependencies import get_post_controller
from src.schemas.data_transfer_objects import PostFullDto


post_router = APIRouter(
    prefix='/post',
    tags=['Посты'],
)


@post_router.get('/many', response_model=list[PostFullDto])
async def get_post_many(
    controller: Annotated[PostController, Depends(get_post_controller)],
):
    return await controller.get_post_many()


@post_router.get('/{post_id}', response_model=PostFullDto)
async def get_post_by_id(
    post_id: Annotated[int, Path(ge=1)],
    controller: Annotated[PostController, Depends(get_post_controller)],
):
    post = await controller.get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail='Пост не найден')
    return post


@post_router.post(
    '',
    response_model=PostFullDto,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post: PostFullDto,
    controller: Annotated[PostController, Depends(get_post_controller)],
):
    return await controller.create_post(post)


@post_router.put('/{post_id}', response_model=PostFullDto)
async def update_post(
    post_id: Annotated[int, Path(ge=1)],
    post: PostFullDto,
    controller: Annotated[PostController, Depends(get_post_controller)],
):
    result = await controller.update_post(post_id, post)
    if result is None:
        raise HTTPException(status_code=404, detail='Пост не найден')
    return result


@post_router.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: Annotated[int, Path(ge=1)],
    controller: Annotated[PostController, Depends(get_post_controller)],
):
    deleted = await controller.delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Пост не найден')
    return None