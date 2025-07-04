from typing import Protocol


class RedisRepositoryProtocol(Protocol):
    async def set(self, key: str, value: str):
        pass

    async def get(self, key: str) -> str:
        pass

    async def delete(self, key: str):
        pass

    async def exists(self, key: str) -> bool:
        pass

    async def getdel(self, key: str) -> str:
        pass
