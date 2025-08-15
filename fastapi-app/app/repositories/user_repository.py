"""User repository interacting with MongoDB."""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.user import UserInDB


class UserRepository:
    """Repository for user CRUD operations."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def get_by_username(self, username: str) -> Optional[UserInDB]:
        """Return a user by username."""
        document = await self.collection.find_one({"username": username})
        if document:
            return UserInDB(**document)
        return None

    async def create(self, user: UserInDB) -> str:
        """Insert a new user and return the username."""
        await self.collection.insert_one(user.model_dump())
        return user.username
