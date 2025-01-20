from domain.interface.repository.base_repository import IBaseRepository
from abc import ABC, abstractmethod


class BaseUnitOfWork(ABC):
    repository: IBaseRepository

    @abstractmethod
    async def __aenter__(self):
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
    