from abc import ABC, abstractmethod
from domain.interface.repository.base_repository import IBaseRepository


class SqlAlchemyAuthRepositoryInterface(IBaseRepository, ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_username(self):
        raise NotImplementedError
    
