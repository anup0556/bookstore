"""Pytest configuration and fixtures."""

import asyncio
import os
import sys
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

# Add necessary directories to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bookstore_dir = os.path.join(project_root, "bookstore")
tests_dir = os.path.dirname(os.path.abspath(__file__))

# Add paths in the correct order
sys.path.insert(0, project_root)  # First priority
sys.path.insert(1, bookstore_dir)  # Second priority
sys.path.insert(2, tests_dir)  # Third priority

from database import get_db
from main import app
from config import TEST_DATABASE_URL, TEST_USER

# Override the database URL for tests
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

# Extract the database file path from the URL
db_file = TEST_DATABASE_URL.replace("sqlite:///", "")

# Create test database engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def pytest_sessionstart(session):
    """
    Called before test session starts.
    Create tables.
    """
    SQLModel.metadata.create_all(test_engine)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished.
    Clean up test database.
    """
    # Close all connections
    test_engine.dispose()

    # Remove the test database file
    try:
        if os.path.exists(db_file):
            os.remove(db_file)
    except Exception as e:
        print(f"Warning: Could not remove test database: {e}")


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before tests and drop them after."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def db_session():
    """Get a TestingSessionLocal instance."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def override_get_db(db_session: Session):
    """Override the get_db dependency."""

    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Create async client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def authenticated_client(
    async_client: AsyncClient,
) -> AsyncGenerator[AsyncClient, None]:
    """Create authenticated client for testing protected endpoints."""
    # Create a test user
    response = await async_client.post("/signup", json=TEST_USER)
    assert response.status_code == 200

    # Login and get token
    response = await async_client.post("/login", json=TEST_USER)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Update client headers with token
    async_client.headers["Authorization"] = f"Bearer {token}"
    yield async_client
