from flask_caching import Cache

from app import app

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': 'redis'})
