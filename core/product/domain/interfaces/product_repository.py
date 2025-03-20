from typing import Protocol
from domain.entities.product import Product


class ProductRepositoryProtocol(Protocol):
    async def get_all(self):
        ...

    async def find_by_name(self, name: str):
        ...

    async def find_by_category(self, category: str):
        ...
