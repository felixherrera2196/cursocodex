"""Pydantic schemas for user operations."""
from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a user."""
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT tokens."""
    access_token: str
    token_type: str = "bearer"
