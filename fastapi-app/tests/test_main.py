"""Tests for the root endpoint."""

import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

# Add fastapi-app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402


@pytest.mark.asyncio
async def test_read_root() -> None:
    """Ensure the root endpoint returns a hello message."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
