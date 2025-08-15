"""Database configuration for MongoDB connection."""
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
_client = AsyncIOMotorClient(MONGO_URI)
_db = _client["app_db"]


def get_user_collection() -> AsyncIOMotorCollection:
    """Return the MongoDB collection for users."""
    return _db["users"]
