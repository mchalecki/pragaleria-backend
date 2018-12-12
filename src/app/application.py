from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from app.config import app_config
from app import app

CONFIG_FILE_LOCATION = Path(__file__).parent / "config.py"
db = SQLAlchemy()


def initialize_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    _register_blueprints(app)
    return app


def _register_blueprints(app):
    from app.resources.api import api_bl

    app.register_blueprint(api_bl)
