from domain.interfaces.repositories.attribute_repository import AttributeRepositoryProtocol
from domain.interfaces.transaction_manager import TransactionManagerProcotol


class GetAllAttributeUseCase:
    def __init__(
        self,
        attribute_repository: AttributeRepositoryProtocol,
    ):
        self.attribute_repository = attribute_repository

    async def execute(self):
        attributes = await self.attribute_repository.get_all()
        return attributes
