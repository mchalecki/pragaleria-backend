from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import app_config
from app.resources.test import test_bl

CONFIG_FILE_LOCATION = Path(__file__).parent / "config.py"
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _add_resources(app)
    db.init_app(app)

    return app


def _add_resources(app):
    app.register_blueprint(test_bl)
