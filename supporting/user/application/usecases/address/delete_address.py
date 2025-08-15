from uuid import UUID
from application.exceptions import AddressNotFoundException
from domain.interfaces.repositories.address_repository import AddressRepository
from domain.interfaces.repositories.user_repository import UserRepository
from domain.interfaces.transaction_manager import TransactionManager
from infrastructure.exceptions import UserNotFoundException


class DeleteUserAddressUseCase:
    def __init__(
    self, 
    user_repository: UserRepository,
    address_repository: AddressRepository,
    transaction_manager: TransactionManager
    ):
        self.user_repository = user_repository
        self.address_repository = address_repository
        self.transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, address_id: UUID) -> UUID:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        address = await self.address_repository.get_by_id(address_id)
        if not address:
            raise AddressNotFoundException(f"Address with id {address_id} not found")
        await self.address_repository.delete(address_id)
        await self.transaction_manager.commit()
        return address_id
