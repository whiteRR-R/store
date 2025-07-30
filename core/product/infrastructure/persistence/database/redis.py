import aioredis


async def redis_client(url: str) -> aioredis.Redis:
    return aioredis.from_url(url)
