from abc import ABC, abstractmethod
from domain.abstacts.repository.base_repository import IBaseRepository


class ISqlAlchemyAuthRepository(IBaseRepository, ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_username(self):
        raise NotImplementedError
    
