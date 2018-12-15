import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.api_utils.caching import cache
from app.configs import current_config

db = SQLAlchemy()


def initialize_app(config):
    app = Flask(__name__)
    # Configs
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # DB
    db.init_app(app)
    # Blueprints
    _register_blueprints(app)
    # Caching
    cache.init_app(app)
    # Logging
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging._nameToLevel[str.upper(current_config.GUNICORN_LOG_LEVEL)])

    return app


def _register_blueprints(app):
    from app.resources.api import api_bl

    app.register_blueprint(api_bl)
