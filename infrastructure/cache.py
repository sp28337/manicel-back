import redis as r

from settings import Settings


def get_redis_connection() -> r.Redis:
    s = Settings()
    return r.Redis(
        host=s.REDIS_HOST,
        port=s.REDIS_PORT,
        db=s.REDIS_DB
    )
