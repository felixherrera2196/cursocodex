"""Data model for users stored in MongoDB."""
from pydantic import BaseModel


class UserInDB(BaseModel):
    """Representation of a user in the database."""
    username: str
    hashed_password: str
