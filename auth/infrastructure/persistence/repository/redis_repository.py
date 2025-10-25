import redis.asyncio as aioredis


class RedisRepository:
    def __init__(self, redis_url: str):
        self.redis_client = aioredis.from_url(redis_url, decode_responses=True)

    async def set(self, key: str, value: str):
        await self.redis_client.set(key, value)

    async def get(self, key: str) -> str:
        return await self.redis_client.get(key)

    async def delete(self, key: str):
        await self.redis_client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.redis_client.exists(key)
    
    async def getdel(self, key: str) -> str:
        return await self.redis_client.getdel(key)
