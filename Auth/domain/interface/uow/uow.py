from typing import Protocol


class UnitOfWorkProtocol(Protocol):  
    async def register_new(self, obj) -> None:
        ...
    
    async def register_dirty(self, obj) -> None:
        ...
        
    async def register_deleted(self, obj) -> None:
        ...
            
    async def commit(self) -> None:
        ...
    
    async def rollback(self) -> None:
        ...
    
    async def clear(self) -> None:
        ...
