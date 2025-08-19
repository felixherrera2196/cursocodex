"""Pydantic schemas for flight operations."""
from datetime import datetime
from pydantic import BaseModel


class FlightCreate(BaseModel):
    """Schema for creating a new flight."""
    id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    seats: int


class Flight(BaseModel):
    """Schema representing flight information."""
    id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    seats: int
