"""Tests for flight endpoints."""
import os
import sys
from datetime import datetime
from pathlib import Path

import mongomock_motor
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402
from app.database import get_flight_collection  # noqa: E402


@pytest_asyncio.fixture
async def flight_collection() -> AsyncIOMotorCollection:
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

    collection = client["test_db"]["flights"]
    await collection.delete_many({})
    app.dependency_overrides[get_flight_collection] = lambda: collection
    try:
        yield collection
    finally:
        await collection.delete_many({})
        app.dependency_overrides.clear()
        client.close()


@pytest.mark.asyncio
async def test_search_and_get_flight(flight_collection: AsyncIOMotorCollection) -> None:
    """Ensure flights can be searched and retrieved."""
    flight = {
        "_id": "AB123",
        "origin": "MEX",
        "destination": "GDL",
        "departure_time": datetime(2023, 1, 1, 10, 0, 0),
        "arrival_time": datetime(2023, 1, 1, 12, 0, 0),
        "price": 1500.0,
    }
    await flight_collection.insert_one(flight)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/flights", params={"origin": "MEX", "destination": "GDL"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "AB123"
        assert data[0]["price"] == 1500.0

        response = await ac.get("/flights/AB123")
        assert response.status_code == 200
        detail = response.json()
        assert detail["origin"] == "MEX"
        assert detail["destination"] == "GDL"
