from typing import Protocol


class TransactionManagerProcotol(Protocol):
    async def commit(self):
        ...
    
    async def rollback(self):
        ...
