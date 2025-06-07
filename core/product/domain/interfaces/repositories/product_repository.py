from domain.aggregates.product import ProductRoot
from uuid import UUID
from typing import Protocol


class ProductRepositoryProtocol(Protocol):
    async def add(self, product: ProductRoot) -> None:
        """
        Adds a new product to the repository.
        """
        ...
    
    async def delete(self, product: ProductRoot) -> None:
        """
        Deletes a product from the repository.
        """
        ...
    
    async def get_all(self) -> list[ProductRoot]:
        """
        Retrieves all products from the repository.
        """
        ...

    async def get_by_id(self, product_id: UUID) -> ProductRoot:
        """
        Gets a product by its ID.
        """
        ...
        
