from uuid import UUID
from application.dtos.address import AddressDTO, UpdateAddressDTO
from application.exceptions import AddressNotFoundException, UserNotFoundException
from application.factories.address_factory import AddressFactory
from domain.interfaces.repositories.address_repository import AddressRepository
from domain.interfaces.repositories.user_repository import UserRepository
from application.common.transaction_manager import TransactionManager


class UpdateUserAddressUseCase:

    def __init__(
    self, 
    user_repository: UserRepository,
    address_repository: AddressRepository,
    transaction_manager: TransactionManager
    ):
        self.user_repository = user_repository
        self.address_repository = address_repository
        self.transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, address_id: UUID, address_dto: UpdateAddressDTO) -> AddressDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        address = await self.address_repository.get_by_id(address_id)
        if not address:
            raise AddressNotFoundException(f"Address with id {address_id} not found")
        
        if address_dto.country and address_dto.city and address_dto.street and address_dto.postal_code:
            address.relocate(address_dto.country, address_dto.city, address_dto.street, address_dto.postal_code)

        if address_dto.city and not (address_dto.country or address_dto.street or address_dto.postal_code):
            address.change_city(address_dto.city)

        if address_dto.apartment is not None:
            address.change_apartment(address_dto.apartment)
        
        await self.address_repository.update(address)
        await self.transaction_manager.commit()
        return AddressFactory.to_dto(address)
