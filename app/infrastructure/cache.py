from redis import asyncio as r

from app.settings import Settings


def get_redis_connection() -> r.Redis:
    s = Settings()
    return r.Redis(host=s.CACHE_HOST, port=s.CACHE_PORT, db=s.CACHE_DB)
