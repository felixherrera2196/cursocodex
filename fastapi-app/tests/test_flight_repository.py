"""Tests for ``FlightRepository``."""

import sys
from datetime import datetime
from pathlib import Path

import mongomock_motor
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.repositories.flight_repository import FlightRepository  # noqa: E402
from app.models.flight import FlightInDB  # noqa: E402


@pytest_asyncio.fixture
async def flight_collection() -> AsyncIOMotorCollection:
    """Provide a mock flight collection."""
    client = mongomock_motor.AsyncMongoMockClient()
    collection = client["test_db"]["flights"]
    await collection.delete_many({})
    try:
        yield collection
    finally:
        await collection.delete_many({})
        client.close()


@pytest.mark.asyncio
async def test_search_and_get_by_id(flight_collection: AsyncIOMotorCollection) -> None:
    """Ensure flights can be searched and retrieved by ID."""
    repo = FlightRepository(flight_collection)
    flight1 = {
        "_id": "AB123",
        "origin": "MEX",
        "destination": "GDL",
        "departure_time": datetime(2023, 1, 1, 10, 0, 0),
        "arrival_time": datetime(2023, 1, 1, 12, 0, 0),
        "price": 1500.0,
        "seats": 1,
    }
    flight2 = {
        "_id": "CD456",
        "origin": "MEX",
        "destination": "CUN",
        "departure_time": datetime(2023, 1, 2, 10, 0, 0),
        "arrival_time": datetime(2023, 1, 2, 12, 0, 0),
        "price": 2000.0,
        "seats": 2,
    }
    await flight_collection.insert_many([flight1, flight2])

    results = await repo.search("MEX", "GDL")
    assert len(results) == 1
    assert results[0].id == "AB123"
    assert results[0].price == 1500.0

    fetched = await repo.get_by_id("AB123")
    assert fetched is not None
    assert fetched.origin == "MEX"

    missing = await repo.get_by_id("ZZ999")
    assert missing is None


@pytest.mark.asyncio
async def test_create_inserts_flight(flight_collection: AsyncIOMotorCollection) -> None:
    """Ensure a flight can be created."""
    repo = FlightRepository(flight_collection)
    flight = FlightInDB(
        id="EF789",
        origin="MEX",
        destination="MTY",
        departure_time=datetime(2023, 1, 3, 10, 0, 0),
        arrival_time=datetime(2023, 1, 3, 12, 0, 0),
        price=1800.0,
        seats=3,
    )
    inserted_id = await repo.create(flight)
    assert inserted_id == "EF789"
    stored = await flight_collection.find_one({"_id": "EF789"})
    assert stored is not None
    assert stored["destination"] == "MTY"
