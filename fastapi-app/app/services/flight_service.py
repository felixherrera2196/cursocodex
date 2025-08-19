"""Service layer for flight operations."""
from typing import List, Optional

from ..models.flight import FlightInDB
from ..repositories.flight_repository import FlightRepository
from ..schemas.flight import FlightCreate


async def search_flights(repo: FlightRepository, origin: str, destination: str) -> List[FlightInDB]:
    """Search flights by origin and destination."""
    return await repo.search(origin, destination)


async def get_flight(repo: FlightRepository, flight_id: str) -> Optional[FlightInDB]:
    """Retrieve a flight by its identifier."""
    return await repo.get_by_id(flight_id)


async def create_flight(repo: FlightRepository, data: FlightCreate) -> FlightInDB:
    """Create a new flight in the repository."""
    flight = FlightInDB(**data.model_dump())
    await repo.create(flight)
    return flight
