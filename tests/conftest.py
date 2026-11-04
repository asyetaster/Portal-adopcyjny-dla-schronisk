"""Wspólne fixtures dla testów pytest."""

import os
import tempfile

import pytest

from app import create_app
from database import init_db


@pytest.fixture()
def app():
    fd, db_path = tempfile.mkstemp(suffix=".db")
    config = {
        "DATABASE_URL": f"sqlite:///{db_path}",
        "SECRET_KEY": "test-secret",
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    }
    application = create_app(config)
    init_db(application.extensions["db_engine"])
    yield application
    application.extensions["db_engine"].dispose()
    os.close(fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()
