from uuid import UUID
from typing import List, Protocol
from application.dtos.product_dto import (
    AttributeDTO, ProductDTO,
    CreateProductDTO, Image
)


class CreateProductUseCaseProtocol(Protocol):
    async def execute(self, product_dto: CreateProductDTO) -> None:
        """Create a new product."""
        pass
    
class DeleteProductUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID) -> None:
        """Delete a product by its ID."""
        pass
    
class GetAllProductsUseCaseProtocol(Protocol):
    async def execute(self) -> List[ProductDTO]:
        """Retrieve all products."""
        pass

class GetProductByIdUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID) -> ProductDTO:
        """Retrieve a product by its ID."""
        pass

class AddProductAttributeUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID, attribute_dto: AttributeDTO) -> None:
        """Add an attribute to a product."""
        pass

class DeleteProductAttributeUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID, attribute_dto: AttributeDTO) -> None:
        """Delete an attribute from a product."""
        pass

class UpdateProductDescriptionUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID, description: str) -> None:
        """Update the description of a product."""
        pass

class UpdateProductPriceUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID, price: int) -> None:
        """Update the price of a product."""
        pass
    
class AddProductImageUseCaseProtocol(Protocol):
    async def execute(self, product_id: UUID, images: List[Image]) -> None:
        """Update the price of a product."""
        pass
