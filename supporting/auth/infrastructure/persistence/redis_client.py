import redis.asyncio as aioredis

        
def get_client(redis_port: int, redis_host: str, redis_password: str):
    """
    Returns an instance of the Redis client.
    """
    return aioredis.from_url(
        f"redis://{redis_host}:{redis_port}",
        decode_responses=True
    )
    

