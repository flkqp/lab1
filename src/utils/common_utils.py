
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from settings import app_settings


password_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)


class CommonUtils:
    """Общие утилиты для авторизации."""

    @staticmethod
    def hash_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        try:
            return password_context.verify(
                plain_password,
                hashed_password,
            )
        except (ValueError, TypeError):
            return False

    @staticmethod
    def create_jwt_token(
        subject: str,
        expires_delta: timedelta,
        token_type: str,
        token_id: int,
    ) -> str:
        expire = datetime.now(timezone.utc) + expires_delta

        payload: dict[str, Any] = {
            'sub': subject,
            'exp': expire,
            'type': token_type,
            'jti': str(token_id),
        }

        return jwt.encode(
            payload,
            app_settings.SECRET_KEY,
            algorithm=app_settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode_jwt_token(token: str) -> dict[str, Any] | None:
        try:
            return jwt.decode(
                token,
                app_settings.SECRET_KEY,
                algorithms=[app_settings.JWT_ALGORITHM],
            )
        except JWTError:
            return None

    @staticmethod
    def create_access_token(user_id: int, token_id: int) -> str:
        return CommonUtils.create_jwt_token(
            subject=str(user_id),
            expires_delta=timedelta(
                minutes=app_settings.ACCESS_TOKEN_EXPIRES_MINUTES
            ),
            token_type='access',
            token_id=token_id,
        )

    @staticmethod
    def create_refresh_token(user_id: int, token_id: int) -> str:
        return CommonUtils.create_jwt_token(
            subject=str(user_id),
            expires_delta=timedelta(
                days=app_settings.REFRESH_TOKEN_EXPIRES_DAYS
            ),
            token_type='refresh',
            token_id=token_id,
        )
