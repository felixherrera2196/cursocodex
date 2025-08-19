"""Tests for reservation service operations."""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models.flight import FlightInDB  # noqa: E402
from app.models.reservation import ReservationInDB  # noqa: E402
from app.services.reservation_service import (  # noqa: E402
    CancellationNotAllowedError,
    cancel_reservation,
)


class FakeFlightRepo:
    """In-memory flight repository for testing."""

    def __init__(self, flight: FlightInDB) -> None:
        self.flight = flight

    async def get_by_id(self, flight_id: str) -> FlightInDB | None:
        return self.flight


class FakeReservationRepo:
    """In-memory reservation repository for testing."""

    def __init__(self, reservation: ReservationInDB) -> None:
        self.reservation = reservation
        self.deleted = False

    async def get_by_id(self, reservation_id: str) -> ReservationInDB | None:
        return self.reservation

    async def delete(self, reservation_id: str) -> None:
        self.deleted = True


@pytest.mark.asyncio
async def test_cancel_reservation_allowed_after_24_hours() -> None:
    """Allow cancellation when flight is more than 24 hours away."""
    now = datetime(2024, 1, 1, 12, 0, 0)
    flight = FlightInDB(
        id="FL1",
        origin="AAA",
        destination="BBB",
        departure_time=now + timedelta(hours=25),
        arrival_time=now + timedelta(hours=26),
        price=100.0,
        seats=1,
    )
    reservation = ReservationInDB(
        id="R1",
        flight_id=flight.id,
        username="alice",
        seat_number=1,
        paid=False,
    )
    flight_repo = FakeFlightRepo(flight)
    reservation_repo = FakeReservationRepo(reservation)

    result = await cancel_reservation(
        flight_repo, reservation_repo, reservation.id, reservation.username, now=now
    )

    assert result == reservation
    assert reservation_repo.deleted is True


@pytest.mark.asyncio
async def test_cancel_reservation_rejected_within_24_hours() -> None:
    """Reject cancellation when flight departs in 24 hours or less."""
    now = datetime(2024, 1, 1, 12, 0, 0)
    flight = FlightInDB(
        id="FL2",
        origin="AAA",
        destination="BBB",
        departure_time=now + timedelta(hours=24),
        arrival_time=now + timedelta(hours=25),
        price=100.0,
        seats=1,
    )
    reservation = ReservationInDB(
        id="R2",
        flight_id=flight.id,
        username="alice",
        seat_number=1,
        paid=False,
    )
    flight_repo = FakeFlightRepo(flight)
    reservation_repo = FakeReservationRepo(reservation)

    with pytest.raises(CancellationNotAllowedError):
        await cancel_reservation(
            flight_repo, reservation_repo, reservation.id, reservation.username, now=now
        )
    assert reservation_repo.deleted is False
