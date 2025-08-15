"""Reservation repository interacting with MongoDB."""
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.reservation import ReservationInDB


class ReservationRepository:
    """Repository for reservation operations."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def count_by_flight(self, flight_id: str) -> int:
        """Count reservations for a given flight."""
        return await self.collection.count_documents({"flight_id": flight_id})

    async def create(self, reservation: ReservationInDB) -> str:
        """Insert a new reservation and return its identifier."""
        document = reservation.model_dump()
        document["_id"] = document.pop("id")
        await self.collection.insert_one(document)
        return reservation.id

    async def list_by_user(self, username: str) -> List[ReservationInDB]:
        """List reservations belonging to a user."""
        cursor = self.collection.find({"username": username})
        results: List[ReservationInDB] = []
        async for document in cursor:
            document["id"] = document.pop("_id")
            results.append(ReservationInDB(**document))
        return results

    async def get_by_id(self, reservation_id: str) -> Optional[ReservationInDB]:
        """Retrieve a reservation by its identifier."""
        document = await self.collection.find_one({"_id": reservation_id})
        if document:
            document["id"] = document.pop("_id")
            return ReservationInDB(**document)
        return None

    async def set_paid(self, reservation_id: str) -> None:
        """Mark a reservation as paid."""
        await self.collection.update_one({"_id": reservation_id}, {"$set": {"paid": True}})
