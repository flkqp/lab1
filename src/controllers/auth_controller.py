from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from settings import app_settings
from src.repositories import (
    AccessTokenRepository,
    RefreshTokenRepository,
    UserRepository,
)
from src.schemas.data_transfer_objects import (
    LoginRequestDto,
    RefreshTokenRequestDto,
    TokenDto,
    VerifyAccessTokenRequestDto,
    VerifyAccessTokenResponseDto,
)
from src.utils.common_utils import CommonUtils


class AuthController:
    """Контроллер аутентификации и управления JWT-токенами."""

    def __init__(
        self,
        user_repository: UserRepository,
        access_token_repository: AccessTokenRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.access_token_repository = access_token_repository
        self.refresh_token_repository = refresh_token_repository

    def _unauthorized(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недействительный или просроченный токен',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    async def _create_tokens(self, user_id: int) -> TokenDto:
        """Создаёт новую пару access- и refresh-токенов."""

        now = datetime.now(timezone.utc)

        refresh_expire = now + timedelta(
            days=app_settings.REFRESH_TOKEN_EXPIRES_DAYS
        )

        refresh_record = await self.refresh_token_repository.create(
            user_id=user_id,
            expire_at=refresh_expire,
        )

        access_expire = now + timedelta(
            minutes=app_settings.ACCESS_TOKEN_EXPIRES_MINUTES
        )

        access_record = await self.access_token_repository.create(
            user_id=user_id,
            refresh_id=refresh_record.id,
            expire_at=access_expire,
        )

        return TokenDto(
            access_token=CommonUtils.create_access_token(
                user_id=user_id,
                token_id=access_record.id,
            ),
            refresh_token=CommonUtils.create_refresh_token(
                user_id=user_id,
                token_id=refresh_record.id,
            ),
        )

    async def _get_user_from_token(
        self,
        token: str,
        expected_type: str,
    ):
        """Проверяет JWT и возвращает пользователя."""

        payload = CommonUtils.decode_jwt_token(token)

        if payload is None or payload.get('type') != expected_type:
            raise self._unauthorized()

        try:
            user_id = int(payload.get('sub'))
            token_id = int(payload.get('jti'))
        except (ValueError, TypeError):
            raise self._unauthorized()

        if expected_type == 'access':
            token_record = await self.access_token_repository.get_by_id(
                token_id
            )
        else:
            token_record = await self.refresh_token_repository.get_by_id(
                token_id
            )

        if token_record is None or token_record.user_id != user_id:
            raise self._unauthorized()

        user = await self.user_repository.get_one_full_by_id(user_id)

        if user is None or getattr(user, 'is_deleted', False):
            raise self._unauthorized()

        return user, token_record

    async def login(self, credentials: LoginRequestDto) -> TokenDto:
        """Проверяет логин и пароль и выдаёт пару токенов."""

        user = await self.user_repository.get_user_by_login(
            credentials.login
        )

        if user is None or not CommonUtils.verify_password(
            credentials.password,
            user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Неверный логин или пароль',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return await self._create_tokens(user.id)

    async def verify_access_token(
        self,
        request: VerifyAccessTokenRequestDto,
    ) -> VerifyAccessTokenResponseDto:
        """Проверяет access-токен."""

        await self._get_user_from_token(
            request.access_token,
            'access',
        )

        return VerifyAccessTokenResponseDto(
            access_token=request.access_token
        )

    async def refresh_tokens(
        self,
        request: RefreshTokenRequestDto,
    ) -> TokenDto:
        """Обновляет пару токенов по действующему refresh-токену."""

        user, refresh_record = await self._get_user_from_token(
            request.refresh_token,
            'refresh',
        )

        await self.refresh_token_repository.delete_by_id(
            refresh_record.id
        )

        return await self._create_tokens(user.id)

    async def logout(
        self,
        request: RefreshTokenRequestDto,
    ) -> dict[str, str]:
        """Удаляет refresh-токен и связанную с ним пару токенов."""

        _, refresh_record = await self._get_user_from_token(
            request.refresh_token,
            'refresh',
        )

        await self.refresh_token_repository.delete_by_id(
            refresh_record.id
        )

        return {'message': 'Выход выполнен успешно'}

    async def delete_expired_tokens(self) -> dict[str, int]:
        """Удаляет просроченные refresh-токены."""

        deleted_count = (
            await self.refresh_token_repository.delete_expired_tokens()
        )

        return {'deleted_count': deleted_count}