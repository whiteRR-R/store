import json
from typing import Any
from redis.asyncio import Redis
from domain.interfaces.repositories.product_repository import ProductRepositoryProtocol


class RedisCacheRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        
    async def get_by_key(self, key: str):
        data = await self.redis.get(key)
        return data
            
    async def set(self, key: str, data: Any):
        await self.redis.set(key, data, ex=120)
    
    async def delete(self, key: str):
        await self.redis.delete(key)
