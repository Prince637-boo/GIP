# tests/conftest.py
import pytest
import asyncio

from fastapi import FastAPI
from httpx import AsyncClient

from tests.utils.db import (
    init_test_db,
    drop_test_db,
    override_get_db,
)
from tests.utils.http import get_test_client

# ============================================
# GLOBAL ASYNC EVENT LOOP (for pytest)
# ============================================
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================
# TEST DATABASE SETUP
# ============================================
@pytest.fixture(scope="session", autouse=True)
async def prepare_test_database():
    """
    Create the test DB once for all tests.
    """
    await init_test_db()
    yield
    await drop_test_db()


# ============================================
# DB SESSION FIXTURE (per-test)
# ============================================
@pytest.fixture
async def db_session():
    """
    One session per test, automatically rolled back.
    """
    from tests.utils.db import AsyncTestingSessionLocal

    async with AsyncTestingSessionLocal() as session:
        transaction = await session.begin()
        yield session
        await transaction.rollback()


# ============================================
# GENERIC CLIENT FIXTURE
# ============================================
@pytest.fixture
async def client(db_session):
    """
    HTTP client available for any service.
    You must override get_db inside the test file.
    """
    # Import must be inside to allow multi-service usage
    from libs.common.database import get_db
    from main import app  # or service-specific main if microservice

    # Override the dependency
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
