from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError

    @abstractmethod
    async def update(self):
        raise NotImplementedError

    
