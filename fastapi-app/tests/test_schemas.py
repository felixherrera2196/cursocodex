"""Tests for schema validation errors."""
import sys
from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.schemas.user import UserCreate  # noqa: E402
from app.schemas.flight import Flight  # noqa: E402
from app.schemas.reservation import Reservation  # noqa: E402


@pytest.mark.parametrize(
    "data",
    [
        {"username": "alice"},  # missing password
        {"username": 123, "password": "secret"},  # wrong type for username
    ],
)
def test_user_create_validation_error(data: dict) -> None:
    """Invalid user data should raise a ValidationError."""
    with pytest.raises(ValidationError):
        UserCreate(**data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "FL1",
            "origin": "A",
            "departure_time": datetime.now(),
            "arrival_time": datetime.now(),
            "price": 100.0,
            "seats": 50,
        },  # missing destination
        {
            "id": "FL1",
            "origin": "A",
            "destination": "B",
            "departure_time": datetime.now(),
            "arrival_time": datetime.now(),
            "price": "free",
            "seats": 50,
        },  # invalid price type
    ],
)
def test_flight_validation_error(data: dict) -> None:
    """Invalid flight data should raise a ValidationError."""
    with pytest.raises(ValidationError):
        Flight(**data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "1",
            "flight_id": "FL1",
            "username": "alice",
            "paid": True,
        },  # missing seat_number
        {
            "id": "1",
            "flight_id": "FL1",
            "username": "alice",
            "seat_number": 12,
            "paid": "maybe",
        },  # invalid paid type
    ],
)
def test_reservation_validation_error(data: dict) -> None:
    """Invalid reservation data should raise a ValidationError."""
    with pytest.raises(ValidationError):
        Reservation(**data)
