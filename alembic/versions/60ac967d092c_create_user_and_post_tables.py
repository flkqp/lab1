
"""create user and post tables

Revision ID: 60ac967d092c
Revises:
Create Date: 2026-11-25 16:36:35.020136
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '60ac967d092c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS post')
    op.execute('CREATE SCHEMA IF NOT EXISTS users')

    op.create_table(
        'post',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Идентификатор'),
        sa.Column('name', sa.String(length=255), nullable=False, comment='Название поста'),
        sa.Column('content', sa.Text(), nullable=False, comment='Контент'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False, comment='Создан'),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Удалено'),
        sa.Column('deleted_by', sa.Integer(), nullable=True, comment='Удалил'),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True, comment='Время удаления'),
        sa.PrimaryKeyConstraint('id'),
        schema='post',
    )

    op.create_index(
        op.f('ix_post_post_id'),
        'post',
        ['id'],
        unique=True,
        schema='post',
    )

    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Идентификатор'),
        sa.Column('username', sa.String(length=50), nullable=False, comment='Никнейм пользователя'),
        sa.Column('email', sa.String(length=120), nullable=False, comment='Почта'),
        sa.Column('login', sa.String(length=255), nullable=False, comment='Логин'),
        sa.Column('password', sa.String(length=255), nullable=False, comment='Пароль'),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Удалено'),
        sa.Column('deleted_by', sa.Integer(), nullable=True, comment='Удалил'),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True, comment='Время удаления'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('login'),
        sa.UniqueConstraint('username'),
        schema='users',
    )

    op.create_index(
        op.f('ix_users_user_id'),
        'user',
        ['id'],
        unique=True,
        schema='users',
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_users_user_id'), table_name='user', schema='users')
    op.drop_table('user', schema='users')

    op.drop_index(op.f('ix_post_post_id'), table_name='post', schema='post')
    op.drop_table('post', schema='post')

    op.execute('DROP SCHEMA IF EXISTS users')
    op.execute('DROP SCHEMA IF EXISTS post')
