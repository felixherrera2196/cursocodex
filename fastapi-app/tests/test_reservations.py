"""Tests for reservation endpoints."""
import sys
from datetime import datetime
from pathlib import Path

import mongomock_motor
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402
from app.database import (  # noqa: E402
    get_flight_collection,
    get_reservation_collection,
    get_user_collection,
)


@pytest_asyncio.fixture
async def setup_collections() -> tuple[AsyncIOMotorCollection, AsyncIOMotorCollection, AsyncIOMotorCollection]:
    """Override MongoDB dependencies with mock collections."""
    client = mongomock_motor.AsyncMongoMockClient()
    user_collection = client["test_db"]["users"]
    flight_collection = client["test_db"]["flights"]
    reservation_collection = client["test_db"]["reservations"]
    await user_collection.delete_many({})
    await flight_collection.delete_many({})
    await reservation_collection.delete_many({})
    app.dependency_overrides[get_user_collection] = lambda: user_collection
    app.dependency_overrides[get_flight_collection] = lambda: flight_collection
    app.dependency_overrides[get_reservation_collection] = lambda: reservation_collection
    try:
        yield user_collection, flight_collection, reservation_collection
    finally:
        await user_collection.delete_many({})
        await flight_collection.delete_many({})
        await reservation_collection.delete_many({})
        app.dependency_overrides.clear()
        client.close()


@pytest.mark.asyncio
async def test_reservation_flow(
    setup_collections: tuple[AsyncIOMotorCollection, AsyncIOMotorCollection, AsyncIOMotorCollection]
) -> None:
    """Ensure reservations can be created, listed, and paid."""
    user_collection, flight_collection, _ = setup_collections
    await flight_collection.insert_one(
        {
            "_id": "AB123",
            "origin": "MEX",
            "destination": "GDL",
            "departure_time": datetime(2023, 1, 1, 10, 0, 0),
            "arrival_time": datetime(2023, 1, 1, 12, 0, 0),
            "price": 1500.0,
            "seats": 1,
        }
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/register", json={"username": "bob", "password": "secret"})
        login = await ac.post("/auth/login", json={"username": "bob", "password": "secret"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.post(
            "/reservations", json={"flight_id": "AB123"}, headers=headers
        )
        assert response.status_code == 201
        reservation = response.json()
        assert reservation["seat_number"] == 1

        response = await ac.post(
            "/reservations", json={"flight_id": "AB123"}, headers=headers
        )
        assert response.status_code == 400

        response = await ac.get("/reservations", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        reservation_id = data[0]["id"]

        response = await ac.post(f"/reservations/{reservation_id}/pay", headers=headers)
        assert response.status_code == 200
        paid = response.json()
        assert paid["paid"] is True
