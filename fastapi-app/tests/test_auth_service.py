"""Tests for authentication service functions."""
import sys
from pathlib import Path

from jose import jwt

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.auth_service import (  # noqa: E402
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing_and_verification() -> None:
    """Ensure hashing and verification behave correctly."""
    password = "s3cret"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_create_access_token_contains_subject() -> None:
    """Ensure JWT token includes the subject claim."""
    token = create_access_token({"sub": "alice"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "alice"
