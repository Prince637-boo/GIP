# tests/utils/http.py
from httpx import AsyncClient

async def get_test_client(app):
    """
    Returns an async HTTP client for testing.
    """
    return AsyncClient(app=app, base_url="http://test")
