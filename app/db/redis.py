import aioredis
import os


REDIS_URL = os.environ.get("REDIS_URL")


async def create_redis_pool():
    redis_pool = await aioredis.from_url(url=REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis_pool
