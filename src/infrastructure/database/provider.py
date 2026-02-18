from contextlib import asynccontextmanager
from typing import AsyncIterator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import text

from src.infrastructure import database_config


class DatabaseProvider:
    """
    Manages the SQLAlchemy async engine lifecycle and session factory.

    Usage in FastAPI lifespan:
        await DatabaseProvider.init_engine()   # startup
        await DatabaseProvider.dispose_engine() # shutdown

    Usage as a FastAPI dependency:
        async def endpoint(session=Depends(DatabaseProvider.get_session)): ...
    """

    _engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    async def init_engine(cls) -> None:
        """Create the engine and connection pool, then verify connectivity."""
        if cls._engine is None:
            logger.debug(
                f"Creating database engine: pool_size={database_config.pool_size}, "
                f"max_overflow={database_config.max_overflow}"
            )
            cls._engine = create_async_engine(
                database_config.async_url,
                pool_size=database_config.pool_size,
                max_overflow=database_config.max_overflow,
            )
            cls._session_maker = async_sessionmaker(
                cls._engine, expire_on_commit=False, class_=AsyncSession
            )
        try:
            async with cls.session_lifecycle() as session:
                await session.execute(text("SELECT 1"))
            logger.debug("Database connection established")
        except Exception:
            logger.error("Database connection error")
            raise

    @classmethod
    async def dispose_engine(cls) -> None:
        """Dispose the engine and release all pooled connections."""
        if cls._engine is not None:
            await cls._engine.dispose()
            logger.debug("Database engine disposed")
            cls._engine = None
            cls._session_maker = None

    @classmethod
    @asynccontextmanager
    async def session_lifecycle(cls) -> AsyncIterator[AsyncSession]:
        """
        Async context manager that yields a session with auto commit/rollback.

        Use this when you need a session outside of FastAPI's DI system.
        """
        if cls._session_maker is None:
            raise RuntimeError("Database engine is not initialised. Call init_engine() first.")
        async with cls._session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                logger.debug("Database session closed")

    @classmethod
    async def get_session(cls) -> AsyncIterator[AsyncSession]:
        """FastAPI dependency that yields a database session."""
        async with cls.session_lifecycle() as session:
            yield session