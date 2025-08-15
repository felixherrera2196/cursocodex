"""Tests for authentication endpoints."""
import os
import sys
from pathlib import Path

import mongomock_motor
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402
from app.database import get_user_collection  # noqa: E402


@pytest_asyncio.fixture(autouse=True)
async def override_dependency() -> None:
    """Override MongoDB dependency with remote or mock collection."""
    mongo_uri = os.getenv("MONGO_URI")
    client = None
    try:
        if mongo_uri:
            client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=2000)
            await client.admin.command("ping")
        else:
            raise RuntimeError("Missing MONGO_URI")
    except Exception:
        client = mongomock_motor.AsyncMongoMockClient()

    collection = client["test_db"]["users"]
    await collection.delete_many({})
    app.dependency_overrides[get_user_collection] = lambda: collection
    yield
    await collection.delete_many({})
    app.dependency_overrides.clear()
    client.close()


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
