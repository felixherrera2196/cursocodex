"""Tests for MongoDB configuration."""

import importlib

import app.database as db


def test_uses_mongo_uri_env(monkeypatch) -> None:
    """Ensure database module reads ``MONGO_URI`` environment variable."""
    monkeypatch.setenv("MONGO_URI", "mongodb://example.com:27017")
    importlib.reload(db)
    assert db.MONGO_URI == "mongodb://example.com:27017"

    monkeypatch.delenv("MONGO_URI", raising=False)
    importlib.reload(db)
    assert db.MONGO_URI == "mongodb://localhost:27017"

