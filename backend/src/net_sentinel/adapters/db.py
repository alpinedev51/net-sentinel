# SQLAlchemy Database Adapter (Async)
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from net_sentinel.config.settings import settings

is_sqlite = settings.DATABASE_URL.startswith("sqlite")

engine_kwargs: dict[str, Any] = {
    "echo": True,  # True - Logs all SQL queries
}

if is_sqlite:
    engine_kwargs.update(
        {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }
    )
else:
    engine_kwargs.update(
        {
            "pool_size": 5,
            "max_overflow": 10,
        }
    )

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to yield an async database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
