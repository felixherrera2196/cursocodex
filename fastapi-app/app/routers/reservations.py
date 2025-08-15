"""Reservation API routes."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorCollection

from ..database import get_flight_collection, get_reservation_collection
from ..repositories.flight_repository import FlightRepository
from ..repositories.reservation_repository import ReservationRepository
from ..schemas.reservation import Reservation, ReservationCreate
from ..services.auth_service import ALGORITHM, SECRET_KEY
from ..services.reservation_service import (
    CancellationNotAllowedError,
    FlightNotFoundError,
    NoSeatsAvailableError,
    ReservationNotFoundError,
    cancel_reservation,
    create_reservation,
    list_reservations,
    pay_reservation,
)

router = APIRouter(prefix="/reservations", tags=["reservations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_flight_repo(
    collection: AsyncIOMotorCollection = Depends(get_flight_collection),
) -> FlightRepository:
    """Provide a flight repository dependency."""
    return FlightRepository(collection)


def get_reservation_repo(
    collection: AsyncIOMotorCollection = Depends(get_reservation_collection),
) -> ReservationRepository:
    """Provide a reservation repository dependency."""
    return ReservationRepository(collection)


async def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    """Decode the JWT token and return the username."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return username
    except JWTError as exc:  # noqa: B904
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


@router.post("", response_model=Reservation, status_code=status.HTTP_201_CREATED)
async def create(
    data: ReservationCreate,
    username: str = Depends(get_current_username),
    flight_repo: FlightRepository = Depends(get_flight_repo),
    reservation_repo: ReservationRepository = Depends(get_reservation_repo),
) -> Reservation:
    """Create a reservation for the current user."""
    try:
        reservation_db = await create_reservation(
            flight_repo, reservation_repo, data.flight_id, username
        )
    except FlightNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    except NoSeatsAvailableError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No seats available")
    return Reservation(**reservation_db.model_dump())


@router.get("", response_model=List[Reservation])
async def list_mine(
    username: str = Depends(get_current_username),
    reservation_repo: ReservationRepository = Depends(get_reservation_repo),
) -> List[Reservation]:
    """List reservations for the current user."""
    reservations_db = await list_reservations(reservation_repo, username)
    return [Reservation(**res.model_dump()) for res in reservations_db]


@router.post("/{reservation_id}/pay", response_model=Reservation)
async def pay(
    reservation_id: str,
    username: str = Depends(get_current_username),
    reservation_repo: ReservationRepository = Depends(get_reservation_repo),
) -> Reservation:
    """Mark a reservation as paid."""
    reservation_db = await pay_reservation(reservation_repo, reservation_id, username)
    if not reservation_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return Reservation(**reservation_db.model_dump())


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel(
    reservation_id: str,
    username: str = Depends(get_current_username),
    flight_repo: FlightRepository = Depends(get_flight_repo),
    reservation_repo: ReservationRepository = Depends(get_reservation_repo),
) -> None:
    """Cancel a reservation for the current user."""
    try:
        await cancel_reservation(flight_repo, reservation_repo, reservation_id, username)
    except ReservationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    except CancellationNotAllowedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancellation allowed only more than 24 hours before departure",
        )
    except FlightNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
