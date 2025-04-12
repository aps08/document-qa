"""
This module provides a utility function to create a database session
using a generator and context manager. It is designed to be used with
FastAPI's `Depends` for dependency injection.
"""

from typing import AsyncGenerator

from config import config
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URL, future=True, echo=config.ECHO
)
async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session using a context manager.

    Yields:
        AsyncSession: The database session.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
