"""Database configuration for MongoDB connection."""
import os
from urllib.parse import urlparse

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/app_db")
_client = AsyncIOMotorClient(MONGO_URI)
_db_name = urlparse(MONGO_URI).path.lstrip("/") or "app_db"
_db = _client[_db_name]


def get_user_collection() -> AsyncIOMotorCollection:
    """Return the MongoDB collection for users."""
    return _db["users"]
