import pytest

from app.application import initialize_app
from app.configs import app_config


@pytest.fixture
def app():
    app = initialize_app(app_config["testing"])
    return app
