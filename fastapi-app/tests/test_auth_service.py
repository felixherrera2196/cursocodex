
"""Tests for authentication service token expiration."""
import asyncio
import sys
from datetime import timedelta
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from jose import jwt
from app.services.auth_service import (  # noqa: E402
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))


from app.main import app  # noqa: E402
from app.services.auth_service import create_access_token  # noqa: E402
from app.routers.reservations import get_reservation_repo  # noqa: E402


class DummyReservationRepo:  # pragma: no cover - used to satisfy dependency
    """Minimal reservation repository for dependency override."""


@pytest_asyncio.fixture(autouse=True)
async def override_reservation_dependency() -> None:
    """Override reservation repository dependency with a dummy repo."""
    app.dependency_overrides[get_reservation_repo] = lambda: DummyReservationRepo()
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_expired_token_returns_401() -> None:
    """Expired tokens should cause protected endpoints to return HTTP 401."""
    token = create_access_token({"sub": "alice"}, expires_delta=timedelta(seconds=1))
    await asyncio.sleep(2)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/reservations", headers=headers)
    assert response.status_code == 401




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

