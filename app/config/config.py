# backend/app/config.py
from datetime import timedelta


class Config:

    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_SECRET_KEY = "jwt_secret_key"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1000000)

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'lardervaultredis.redis.cache.windows.net'
    CACHE_REDIS_PORT = 6380
    CACHE_REDIS_PASSWORD = 'kaYgyir0txdrrLpHnMCHCy4ktfLnKG2EHAzCaLaIoIo='
    CACHE_REDIS_SSL = True    
    CACHE_DEFAULT_TIMEOUT= 300
     

