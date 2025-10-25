from typing import Protocol


class TransactionManagerProtocol(Protocol):
    async def commit(self):
        ...

    async def rollback(self):
        ...
