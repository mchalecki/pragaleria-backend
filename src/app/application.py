from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import app_config
from app.resources.mocks import mocks_bl
from app.resources.test import test_bl

CONFIG_FILE_LOCATION = Path(__file__).parent / "config.py"
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    _register_blueprints(app)

    return app


def _register_blueprints(app):
    from app.resources.api import api_bl
    from app.resources.mocks import mocks_bl
    from app.resources.test import test_bl

    app.register_blueprint(api_bl)
    app.register_blueprint(test_bl)
    app.register_blueprint(mocks_bl)
