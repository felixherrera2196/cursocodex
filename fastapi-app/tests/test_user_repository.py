"""Tests for ``UserRepository``."""

import sys
from pathlib import Path

import mongomock_motor
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.repositories.user_repository import UserRepository  # noqa: E402
from app.models.user import UserInDB  # noqa: E402


@pytest_asyncio.fixture
async def user_collection() -> AsyncIOMotorCollection:
    """Provide a mock user collection."""
    client = mongomock_motor.AsyncMongoMockClient()
    collection = client["test_db"]["users"]
    await collection.delete_many({})
    try:
        yield collection
    finally:
        await collection.delete_many({})
        client.close()


@pytest.mark.asyncio
async def test_create_and_get_user(user_collection: AsyncIOMotorCollection) -> None:
    """Ensure users can be created and retrieved."""
    repo = UserRepository(user_collection)
    user = UserInDB(username="alice", hashed_password="secret")
    username = await repo.create(user)
    assert username == "alice"
    assert await user_collection.count_documents({}) == 1

    fetched = await repo.get_by_username("alice")
    assert fetched is not None
    assert fetched.username == "alice"
    assert fetched.hashed_password == "secret"


@pytest.mark.asyncio
async def test_get_missing_user(user_collection: AsyncIOMotorCollection) -> None:
    """Ensure ``None`` is returned when user is absent."""
    repo = UserRepository(user_collection)
    fetched = await repo.get_by_username("missing")
    assert fetched is None
