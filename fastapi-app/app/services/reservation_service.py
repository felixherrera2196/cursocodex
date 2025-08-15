"""Service layer for reservation operations."""
from typing import List
from uuid import uuid4

from ..models.reservation import ReservationInDB
from ..repositories.flight_repository import FlightRepository
from ..repositories.reservation_repository import ReservationRepository


class FlightNotFoundError(Exception):
    """Raised when the flight does not exist."""


class NoSeatsAvailableError(Exception):
    """Raised when the flight has no available seats."""


async def create_reservation(
    flight_repo: FlightRepository,
    reservation_repo: ReservationRepository,
    flight_id: str,
    username: str,
) -> ReservationInDB:
    """Create a reservation if seats are available."""
    flight = await flight_repo.get_by_id(flight_id)
    if not flight:
        raise FlightNotFoundError
    reserved = await reservation_repo.count_by_flight(flight_id)
    if reserved >= flight.seats:
        raise NoSeatsAvailableError
    seat_number = reserved + 1
    reservation = ReservationInDB(
        id=str(uuid4()),
        flight_id=flight_id,
        username=username,
        seat_number=seat_number,
        paid=False,
    )
    await reservation_repo.create(reservation)
    return reservation


async def list_reservations(
    reservation_repo: ReservationRepository, username: str
) -> List[ReservationInDB]:
    """List reservations for a given user."""
    return await reservation_repo.list_by_user(username)


async def pay_reservation(
    reservation_repo: ReservationRepository, reservation_id: str, username: str
) -> ReservationInDB | None:
    """Mark a reservation as paid if it belongs to the user."""
    reservation = await reservation_repo.get_by_id(reservation_id)
    if not reservation or reservation.username != username:
        return None
    await reservation_repo.set_paid(reservation_id)
    reservation.paid = True
    return reservation
