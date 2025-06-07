from typing import List, Protocol
from application.dtos.product_dto import ProductDTO
from uuid import UUID


class CreateProductUseCaseProtocol(Protocol):
    async def execute(self, product_dto: ProductDTO) -> None:
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
