from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.api_utils.caching import cache

db = SQLAlchemy()


def initialize_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    _register_blueprints(app)
    cache.init_app(app)
    return app


def _register_blueprints(app):
    from app.resources.api import api_bl

    app.register_blueprint(api_bl)
