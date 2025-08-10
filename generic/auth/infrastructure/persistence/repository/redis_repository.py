from redis.asyncio import Redis


class RedisRepository:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

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
