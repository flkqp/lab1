from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import app_settings
from .common_factories import get_sqlalchemy_async_session_generator


db_engine = create_async_engine(
    app_settings.SQL_DSN,
    echo=True,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
)

sqlalchemy_async_session_generator = (
    get_sqlalchemy_async_session_generator(async_session_factory)
)