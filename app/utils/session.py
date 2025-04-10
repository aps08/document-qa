"""
This module provides a utility function to create a database session
using a generator and context manager. It is designed to be used with
FastAPI's `Depends` for dependency injection.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from config.configuration import config

engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session using a context manager.

    Yields:
        AsyncSession: The database session.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
