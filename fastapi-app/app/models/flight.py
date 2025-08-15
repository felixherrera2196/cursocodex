"""Data model for flights stored in MongoDB."""
from datetime import datetime
from pydantic import BaseModel


class FlightInDB(BaseModel):
    """Representation of a flight in the database."""
    id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
