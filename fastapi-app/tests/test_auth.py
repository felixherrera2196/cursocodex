"""Tests for authentication endpoints."""
import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
import mongomock_motor

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402
from app.database import get_user_collection  # noqa: E402


@pytest.fixture(autouse=True)
def override_dependency():
    """Override MongoDB dependency with an in-memory mock."""
    client = mongomock_motor.AsyncMongoMockClient()
    collection = client["test_db"]["users"]
    app.dependency_overrides[get_user_collection] = lambda: collection
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_and_login() -> None:
    """Ensure a user can register and then log in to receive a token."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={"username": "alice", "password": "secret"})
        assert response.status_code == 200
        assert response.json() == "alice"

        response = await ac.post("/auth/login", json={"username": "alice", "password": "secret"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
