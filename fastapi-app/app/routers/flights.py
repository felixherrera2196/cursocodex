"""Flight API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorCollection

from ..database import get_flight_collection
from ..repositories.flight_repository import FlightRepository
from ..schemas.flight import Flight, FlightCreate
from ..services.flight_service import create_flight, get_flight, search_flights

router = APIRouter(prefix="/flights", tags=["flights"])


def get_flight_repo(collection: AsyncIOMotorCollection = Depends(get_flight_collection)) -> FlightRepository:
    """Provide a flight repository dependency."""
    return FlightRepository(collection)


@router.get("", response_model=List[Flight])
async def search(
    origin: str = Query(...),
    destination: str = Query(...),
    repo: FlightRepository = Depends(get_flight_repo),
) -> List[Flight]:
    """Search for flights by origin and destination."""
    flights_db = await search_flights(repo, origin, destination)
    return [Flight(**flight.model_dump()) for flight in flights_db]


@router.get("/{flight_id}", response_model=Flight)
async def get(flight_id: str, repo: FlightRepository = Depends(get_flight_repo)) -> Flight:
    """Retrieve detailed information about a flight."""
    flight_db = await get_flight(repo, flight_id)
    if not flight_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    return Flight(**flight_db.model_dump())


@router.post("", response_model=Flight, status_code=status.HTTP_201_CREATED)
async def create(
    data: FlightCreate, repo: FlightRepository = Depends(get_flight_repo)
) -> Flight:
    """Create a new flight."""
    flight_db = await create_flight(repo, data)
    return Flight(**flight_db.model_dump())
