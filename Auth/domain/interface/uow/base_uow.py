from typing import Protocol


class UnitOfWorkProtocol(Protocol):  
    async def register_new(self, obj) -> None:
        """ Регистрирует новый объект. """
        ...
    
    async def register_dirty(self, obj) -> None:
        """ Регистрирует измененный объект. """
        ...
        
    async def register_deleted(self, obj) -> None:
        """ Регистрирует удаленный объект. """
        ...
            
    async def commit(self) -> None:
        """ Подтверждает текущую транзакцию. """
        ...
    
    async def rollback(self) -> None:
        """ Откатывает текущую транзакцию. """
        ...
    
    async def clear(self) -> None:
        """ Очищает списки объектов. """
        ...
