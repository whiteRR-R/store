from domain.interface.repository.base_repository import IBaseRepository
from abc import ABC, abstractmethod


class BaseUnitOfWork(ABC):  

    @property
    @abstractmethod
    def repository(self) -> IBaseRepository:
        raise NotImplementedError

    @abstractmethod
    async def register_new(self, obj):
        raise NotImplementedError
    
    @abstractmethod
    async def register_dirty(self, obj):
        raise NotImplementedError
        
    @abstractmethod    
    async def register_deleted(self, obj):
        raise NotImplementedError
            
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
    
    @abstractmethod
    async def clear(self):
        raise NotImplementedError
    