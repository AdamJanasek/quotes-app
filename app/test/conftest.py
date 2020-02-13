import pytest

from app import create_app
from app.controllers.api import FavQsApi


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def api():
    return FavQsApi
