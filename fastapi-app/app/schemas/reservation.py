"""Pydantic schemas for reservation operations."""
from pydantic import BaseModel


class ReservationCreate(BaseModel):
    """Schema for creating a reservation."""
    flight_id: str


class Reservation(BaseModel):
    """Schema representing reservation information."""
    id: str
    flight_id: str
    username: str
    seat_number: int
    paid: bool
