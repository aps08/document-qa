"""
This module provides shared fixtures for pytest to set up the testing environment.
It includes database setup, event loop management, and an HTTP client for testing FastAPI applications.
"""

import io
import asyncio
import os
import sys
from typing import AsyncGenerator
import warnings
from dotenv import load_dotenv
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import text

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from app.models import Base
from app.main import app

load_dotenv()

test_engine = create_async_engine(
    os.getenv("TEST_SQLALCHEMY_DATABASE_URL"),
    future=True,
    echo=False,
)

test_async_session_factory = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Create a session-scoped event loop for async tests and fixtures.
    Ensures the event loop only closes after all tests are run.

    Scope: session
    - This fixture is shared across all tests in the session.
    - It ensures that the event loop remains active for the entire test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """
    Set up the test database by creating all tables before the tests run.
    Drops all tables after the tests are completed.

    Scope: session
    - This fixture is automatically executed once per test session.
    - It ensures that the database schema is prepared for testing.
    """
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session for tests.

    Yields:
        AsyncSession: The database session.

    Scope: session
    - This fixture is shared across all tests in the session.
    - It provides a single database session for the entire test session.
    """
    async with test_async_session_factory() as session:
        try:
            
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture(scope="module")
async def app_client():
    """
    Create an asynchronous test client for FastAPI.

    Yields:
        AsyncClient: The HTTP client for making API requests.

    Scope: module
    - This fixture is shared across all tests in a single module.
    - It provides an HTTP client for testing FastAPI endpoints.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def sample_document():
    """
    Provides a sample document for testing.
    """
    return {
        "filename": "sample.pdf",
        "status": "COMPLETED",
        "embedding_model": "text-embedding-3-small",
        "processing_time": 12.34,
        "metadata_info": {"size": "150 KB", "pages": 10, "md5": "abc123"},
        "is_deleted": False,
    }


@pytest.fixture
def sample_pdf():
    """
    Provides a mock PDF document for testing.
    """
    pdf_path = os.path.join(os.path.dirname(__file__), "../docs/pdf/wikipedia-4.pdf")
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()
    pdf_file = io.BytesIO(pdf_content)
    pdf_file.name = "mock_document.pdf"
    return pdf_file


@pytest.fixture
def session_payload():
    """
    Provides a mock create chat session payload.
    """
    return {
        "name": "Chat Session",
        "document_id": 100,
        "system_message": "Results in pointers.",
    }
    

@pytest.fixture
def chat_payload():
    """
    Provides a mock chat payload.
    """
    return {
        "question": "Provide the summary of the file",
        "model": "gpt-4-turbo",
        "max_tokens": 300,
    }
