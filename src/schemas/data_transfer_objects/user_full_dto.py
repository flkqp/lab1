from pydantic import Field
from src.schemas.common import MixinIdSchema, MixinSoftDeleteSchema


class UserFullDto(MixinIdSchema, MixinSoftDeleteSchema):
    """Полный DTO пользователя."""

    username: str = Field(description='Никнейм', examples=['Username'])
    email: str = Field(description='Почта', examples=['example@mail.com'])
    login: str = Field(description='Логин', examples=['login'])
    password: str = Field(description='Пароль', examples=['qwerty'])