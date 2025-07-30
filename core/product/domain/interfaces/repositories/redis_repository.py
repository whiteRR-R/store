from typing import Any, Protocol


class RedisCacheRepositoryProtocol:
    async def get_by_key(self, key: str):
        ...

    async def set(self, key: str, data: Any):
        ...
