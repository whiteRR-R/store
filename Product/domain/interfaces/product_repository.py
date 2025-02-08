from abc import ABC, abstractmethod


class ProductRepository(ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_name(self, name: str):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_category(self):
        raise NotImplementedError
    
