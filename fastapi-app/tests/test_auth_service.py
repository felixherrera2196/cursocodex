"""Tests for authentication service token expiration."""
import asyncio
import sys
from datetime import timedelta
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

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
