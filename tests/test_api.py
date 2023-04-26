import pytest
from httpx import AsyncClient
import os

TEST_ENV = os.getenv("TEST_ENV")


@pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
@pytest.mark.asyncio
async def test_root_is_up():
    from api.fast_api import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
@pytest.mark.asyncio
async def test_root_returns_greeting():
    from api.fast_api import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.json() == {"greeting":
        "Welcome to the Book Club Ranked Choice Voting API!"}


@pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
@pytest.mark.asyncio
async def test_get_results_is_up():
    from api.fast_api import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/get_results")
    assert response.status_code == 200


@pytest.mark.skipif(TEST_ENV != "development", reason="only dev mode")
@pytest.mark.asyncio
async def test_get_results_is_str():
    from api.fast_api import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("get_results")
    assert isinstance(response.json(), str)
    assert len(response.json()) == 1
