from multiprocessing import cpu_count
from os import environ

from app.configs import app_config


def max_workers():
    return 2 * cpu_count() + 1


def gunicorn_log_level():
    config = app_config[environ.get('config', 'development')]
    return config.GUNICORN_LOG_LEVEL


bind = '0.0.0.0:' + environ.get('PORT', '8000')
max_requests = 1000
loglevel = gunicorn_log_level()
worker_class = 'gevent'
workers = max_workers()
errorlog = "/logs/errorlog.log"
