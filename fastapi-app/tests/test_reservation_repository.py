"""Tests for ``ReservationRepository``."""

import sys
from pathlib import Path

import mongomock_motor
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.repositories.reservation_repository import ReservationRepository  # noqa: E402
from app.models.reservation import ReservationInDB  # noqa: E402


@pytest_asyncio.fixture
async def reservation_collection() -> AsyncIOMotorCollection:
    """Provide a mock reservation collection."""
    client = mongomock_motor.AsyncMongoMockClient()
    collection = client["test_db"]["reservations"]
    await collection.delete_many({})
    try:
        yield collection
    finally:
        await collection.delete_many({})
        client.close()


@pytest.mark.asyncio
async def test_create_count_get_and_delete(reservation_collection: AsyncIOMotorCollection) -> None:
    """Ensure reservations can be created, counted, retrieved and deleted."""
    repo = ReservationRepository(reservation_collection)
    res1 = ReservationInDB(id="r1", flight_id="f1", username="alice", seat_number=1, paid=False)
    res2 = ReservationInDB(id="r2", flight_id="f1", username="bob", seat_number=2, paid=False)
    res3 = ReservationInDB(id="r3", flight_id="f2", username="alice", seat_number=1, paid=False)
    await repo.create(res1)
    await repo.create(res2)
    await repo.create(res3)

    assert await reservation_collection.count_documents({}) == 3
    assert await repo.count_by_flight("f1") == 2

    fetched = await repo.get_by_id("r1")
    assert fetched is not None
    assert fetched.username == "alice"

    await repo.delete("r1")
    assert await repo.get_by_id("r1") is None
    assert await repo.count_by_flight("f1") == 1
