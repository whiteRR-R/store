from abc import ABC, abstractmethod
from domain.entities.user import User
from domain.interface.repository.base_repository import IBaseRepository


class AuthRepositoryInterface(IBaseRepository, ABC):    
    @abstractmethod
    async def find_by_username(self, username: str):
        raise NotImplementedError
    
    async def find_by_email(self, email: str):
        raise NotImplementedError
    
    async def update(self, user: User):
        raise NotImplementedError
