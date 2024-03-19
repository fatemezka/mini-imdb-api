import os
from app.db.redis import create_redis_pool
from app.utils.error_handler import ErrorHandler


class RedisController:
    async def __init__(self):
        self.redis_pool = await create_redis_pool()

    async def get_allowed_ip_list(self):
        allowed_ip_list = await self.redis_pool.lrange("allowed_ip_list", 0, -1) or []
        return allowed_ip_list

    async def increase_request_attempts(self, ip):
        existing_redis_ip = await self.get_value(ip)
        if not existing_redis_ip:
            await self.redis_pool.setex(name=ip, time=60, value=1)
            return
        counter = int(await self.redis_pool.get(name=ip))
        if counter >= 5:
            raise ErrorHandler.too_many_request()

        counter += 1
        remaining_ttl = await self.redis_pool.ttl(ip)
        await self.redis_pool.setex(name=ip, time=remaining_ttl, value=counter)

    async def store_token(self, user, token):
        redis_key = user.email
        redis_value = token

        # set to redis
        ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        await self.redis_pool.setex(
            name=redis_key,
            time=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            value=redis_value)

    async def remove_token(self, user):
        redis_key = user.email
        check_redis_key = await self.redis_pool.get(name=redis_key)
        if check_redis_key:
            await self.redis_pool.delete(redis_key)

    async def get_value(self, key):
        check_redis_key = await self.redis_pool.get(name=key)
        return bool(check_redis_key)
