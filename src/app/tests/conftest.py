import pytest

from app.application import initialize_app


@pytest.fixture
def app():
    app = initialize_app("testing")
    return app
