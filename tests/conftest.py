import pytest
from flask import Flask, testing

from core.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app: Flask) -> testing.FlaskClient:
    return app.test_client()
