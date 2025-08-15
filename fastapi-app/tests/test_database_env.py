"""Tests for MongoDB configuration."""

import importlib

import app.database as db


def test_uses_mongo_uri_env(monkeypatch) -> None:
    """Ensure database uses ``MONGO_URI`` environment variable and database name."""
    uri = "mongodb://example.com:27017/remote_db"
    monkeypatch.setenv("MONGO_URI", uri)
    importlib.reload(db)
    assert db.MONGO_URI == uri
    assert db.get_user_collection().database.name == "remote_db"


def test_defaults_to_local(monkeypatch) -> None:
    """Ensure local settings are used when ``MONGO_URI`` is unset."""
    monkeypatch.delenv("MONGO_URI", raising=False)
    importlib.reload(db)
    assert db.MONGO_URI == "mongodb://localhost:27017/app_db"
    assert db.get_user_collection().database.name == "app_db"

