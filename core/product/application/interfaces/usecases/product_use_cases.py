from typing import List, Protocol
from application.dtos.product_dto import AttributeDTO, ProductDTO, CreateProductDTO
from uuid import UUID


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
