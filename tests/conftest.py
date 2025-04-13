import asyncio
import os
import sys
from typing import AsyncGenerator
import warnings
from dotenv import load_dotenv
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from app.models import Base
from app.utils import get_db_session
from fastapi.testclient import TestClient
from app.main import app


load_dotenv()
test_engine = create_async_engine(
    os.getenv("TEST_SQLALCHEMY_DATABASE_URL"), 
    future=True, 
    echo=False
)

test_async_session_factory = async_sessionmaker(
    bind=test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Create a session-scoped event loop for async tests and fixtures.
    Ensures the event loop only closes after all tests are run.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
    print("Closed loop")


@pytest.fixture(autouse=True)
async def setup_database():
    """Set up the test database by creating all tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session for tests.
    
    Yields:
        AsyncSession: The database session.
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


@pytest.fixture(scope="function")
def override_get_db_session(db_session):
    """
    Override the get_db_session dependency to use the test database session.
    """
    async def _override_get_db_session():
        yield db_session
    
    return _override_get_db_session


@pytest.fixture(scope="function")
def app_client(override_get_db_session):
    """
    Create a test client for FastAPI.
    """
    app.dependency_overrides[get_db_session] = override_get_db_session
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}