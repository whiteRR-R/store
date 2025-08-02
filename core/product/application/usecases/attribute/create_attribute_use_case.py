from domain.value_objects.product_attribute import ProductAttribute
from domain.interfaces.transaction_manager import TransactionManagerProcotol
from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from application.dtos.attribute_dto import AttributeDTO


class CreateAttributeUseCase:
    def __init__(
        self,
        attribute_repository: AttributeRepositoryProtocol,
        transaction_manager: TransactionManagerProcotol,
    ):
        self.attribute_repository = attribute_repository
        self.transaction_manager = transaction_manager

    async def execute(self, attribute_dto: AttributeDTO):
        await self.attribute_repository.add(attribute_dto.key)
        await self.transaction_manager.commit()
