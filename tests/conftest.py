import os
import tempfile

import pytest

fd, test_db_path = tempfile.mkstemp(suffix=".db")
os.close(fd)

os.environ["DATABASE_URL"] = f"sqlite:///{test_db_path}"

from app import app
from models import db


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database():
    yield

    with app.app_context():
        db.session.remove()
        db.drop_all()

    if os.path.exists(test_db_path):
        os.remove(test_db_path)