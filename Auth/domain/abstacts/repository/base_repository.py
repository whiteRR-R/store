from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def update(self):
        pass

    
