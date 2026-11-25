
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.controllers import UserController
from src.dependencies.controllers_dependencies import get_user_controller
from src.schemas.data_transfer_objects import UserFullDto


user_router = APIRouter(
    prefix='/user',
    tags=['Пользователи'],
)


@user_router.get(
    '/many',
    response_model=list[UserFullDto],
    response_model_exclude={'password'},
)
async def get_user_many(
    controller: Annotated[UserController, Depends(get_user_controller)],
):
    return await controller.get_user_many()


@user_router.get(
    '/{user_id}',
    response_model=UserFullDto,
    response_model_exclude={'password'},
)
async def get_user_by_id(
    user_id: Annotated[int, Path(ge=1)],
    controller: Annotated[UserController, Depends(get_user_controller)],
):
    user = await controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return user


@user_router.post(
    '',
    response_model=UserFullDto,
    response_model_exclude={'password'},
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserFullDto,
    controller: Annotated[UserController, Depends(get_user_controller)],
):
    return await controller.create_user(user)


@user_router.put(
    '/{user_id}',
    response_model=UserFullDto,
    response_model_exclude={'password'},
)
async def update_user(
    user_id: Annotated[int, Path(ge=1)],
    user: UserFullDto,
    controller: Annotated[UserController, Depends(get_user_controller)],
):
    result = await controller.update_user(user_id, user)
    if result is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return result


@user_router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: Annotated[int, Path(ge=1)],
    controller: Annotated[UserController, Depends(get_user_controller)],
):
    deleted = await controller.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return None
