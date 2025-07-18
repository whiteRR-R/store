from application.dtos.brand_dto import CreateBrandDTO, BrandDTO
from typing import Protocol, TypeVar
from uuid import UUID


class CreateBrandUseCaseProtocol(Protocol):
    async def execute(self, brand_dto: CreateBrandDTO) -> None:
        """Create a new brand."""
        pass


class DeleteBrandUseCaseProtocol(Protocol):
    async def execute(self, brand_id: UUID) -> None:
        """Delete a brand by its ID."""
        pass


class GetAllBrandsUseCaseProtocol(Protocol):
    async def execute(self) -> list[BrandDTO]:
        """Get all brands."""
        pass
