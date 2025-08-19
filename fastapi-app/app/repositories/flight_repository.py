"""Flight repository interacting with MongoDB."""
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.flight import FlightInDB


class FlightRepository:
    """Repository for flight operations."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def search(self, origin: str, destination: str) -> List[FlightInDB]:
        """Return flights matching origin and destination."""
        cursor = self.collection.find({"origin": origin, "destination": destination})
        results = []
        async for document in cursor:
            document["id"] = document.pop("_id")
            results.append(FlightInDB(**document))
        return results

    async def get_by_id(self, flight_id: str) -> Optional[FlightInDB]:
        """Return a flight by its identifier."""
        document = await self.collection.find_one({"_id": flight_id})
        if document:
            document["id"] = document.pop("_id")
            return FlightInDB(**document)
        return None

    async def create(self, flight: FlightInDB) -> str:
        """Insert a new flight and return its identifier."""
        document = flight.model_dump()
        document["_id"] = document.pop("id")
        await self.collection.insert_one(document)
        return flight.id
