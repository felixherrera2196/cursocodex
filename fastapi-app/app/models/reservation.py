"""Data model for reservations stored in MongoDB."""
from pydantic import BaseModel


class ReservationInDB(BaseModel):
    """Representation of a reservation in the database."""
    id: str
    flight_id: str
    username: str
    seat_number: int
    paid: bool = False
