
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.dependencies.repositories_dependencies import (
    get_access_token_repository,
    get_user_repository,
)
from src.repositories import AccessTokenRepository, UserRepository
from src.utils.common_utils import CommonUtils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    access_token_repository: Annotated[
        AccessTokenRepository,
        Depends(get_access_token_repository),
    ],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить токен',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    payload = CommonUtils.decode_jwt_token(token)

    if payload is None or payload.get('type') != 'access':
        raise credentials_exception

    try:
        user_id = int(payload.get('sub'))
        token_id = int(payload.get('jti'))
    except (ValueError, TypeError):
        raise credentials_exception

    token_record = await access_token_repository.get_by_id(token_id)

    if token_record is None or token_record.user_id != user_id:
        raise credentials_exception

    user = await user_repository.get_one_full_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user
