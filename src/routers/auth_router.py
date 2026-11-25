from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.controllers import AuthController
from src.dependencies.controllers_dependencies import get_auth_controller
from src.schemas.data_transfer_objects import (
    LoginRequestDto,
    RefreshTokenRequestDto,
    TokenDto,
    VerifyAccessTokenRequestDto,
    VerifyAccessTokenResponseDto,
)


auth_router = APIRouter(
    prefix='/auth',
    tags=['Авторизация'],
)


@auth_router.post(
    '/login',
    response_model=TokenDto,
)
async def login(
    credentials: LoginRequestDto,
    controller: Annotated[
        AuthController,
        Depends(get_auth_controller),
    ],
):
    return await controller.login(credentials)


@auth_router.post(
    '/verify_access_token',
    response_model=VerifyAccessTokenResponseDto,
)
async def verify_access_token(
    request: VerifyAccessTokenRequestDto,
    controller: Annotated[
        AuthController,
        Depends(get_auth_controller),
    ],
):
    return await controller.verify_access_token(request)


@auth_router.post(
    '/refresh_tokens',
    response_model=TokenDto,
)
async def refresh_tokens(
    request: RefreshTokenRequestDto,
    controller: Annotated[
        AuthController,
        Depends(get_auth_controller),
    ],
):
    return await controller.refresh_tokens(request)


@auth_router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
)
async def logout(
    request: RefreshTokenRequestDto,
    controller: Annotated[
        AuthController,
        Depends(get_auth_controller),
    ],
):
    return await controller.logout(request)


@auth_router.delete(
    '/expired_tokens',
    status_code=status.HTTP_200_OK,
)
async def delete_expired_tokens(
    controller: Annotated[
        AuthController,
        Depends(get_auth_controller),
    ],
):
    return await controller.delete_expired_tokens()