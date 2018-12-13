import os


class Config:
    """Parent configuration class."""
    GUNICORN_LOG_LEVEL = 'info'
    DEBUG = False
    CACHE_TIMEOUT = 60
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@db/{}?charset=utf8&use_unicode=0'.format(
        os.getenv('MYSQL_ROOT_PASSWORD'),
        os.getenv('MYSQL_DATABASE'),
    )


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    CACHE_TIMEOUT = 30
    GUNICORN_LOG_LEVEL = 'debug'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    GUNICORN_LOG_LEVEL = 'debug'


class ProductionConfig(Config):
    """Configuration for production"""
    DEBUG = False
    CACHE_TIMEOUT = 600
    GUNICORN_LOG_LEVEL = 'warning'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
current_config = app_config[os.environ['config']]
