from uuid import UUID
from application.dtos.address import AddressDTO
from application.exceptions import UserNotFoundException
from application.factories.address_factory import AddressFactory
from domain.interfaces.repositories.address_repository import AddressRepository
from domain.interfaces.repositories.user_repository import UserRepository
from domain.interfaces.transaction_manager import TransactionManager


class AddUserAddressUseCase:
    def __init__(
    self, 
    user_repository: UserRepository,
    address_repository: AddressRepository,
    transaction_manager: TransactionManager
    ):
        self.user_repository = user_repository
        self.address_repository = address_repository
        self.transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, address_dto: AddressDTO) -> AddressDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        address = AddressFactory.from_dto(address_dto)
        await self.address_repository.add(address)
        await self.transaction_manager.commit()
        return address_dto
