from abc import ABC, abstractmethod
from domain.entities.product import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, product: Product):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, product: Product):
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_name(self, name: str):
        raise NotImplementedError

    
    @abstractmethod
    async def find_by_category(self, category: str):
        raise NotImplementedError
    
