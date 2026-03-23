import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_async_session
from app.config import get_settings
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient


# Use test database
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client():
    """Create an async client for testing"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="module")
def client():
    """Create a test client for sync tests"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
async def test_db():
    """Setup test database"""
    settings = get_settings()

    # Create test database URL
    test_db_url = settings.DATABASE_URL.replace("clawith", "test_clawith")

    # Create engine and tables
    engine = create_async_engine(test_db_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield async_session

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(test_db):
    """Create a database session for each test"""
    async with test_db() as session:
        yield session


@pytest.fixture
async def authenticated_client(client):
    """Create a client with authentication"""
    # Create a user and login to get token
    # For now, return the client as is
    # This would be expanded with actual auth logic
    yield client