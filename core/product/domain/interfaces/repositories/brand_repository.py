from domain.entities.brand import Brand
from typing import Protocol
from uuid import UUID


class BrandRepositoryProtocol(Protocol):
    async def create(self, brand: Brand) -> None:
        """
        Adds a new brand to the repository.
        """
        ...
    
    async def get_all(self) -> list[Brand]:
        """
        Retrieves all brands from the repository.
        """
        ...
    
    async def get_by_id(self, brand_id: UUID) -> Brand:
        """
        Gets a brand by its ID.
        """
        ...

    async def delete(self, brand: Brand) -> None:
        """
        Deletes a brand from the repository.
        """
        ...
