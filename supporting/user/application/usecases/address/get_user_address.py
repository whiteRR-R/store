from uuid import UUID
from application.exceptions import AddressNotFoundException, UserNotFoundException
from domain.interfaces.repositories.address_repository import AddressRepository
from domain.interfaces.repositories.user_repository import UserRepository


class GetUserAddressUseCase:
    def __init__(
    self, 
    user_repository: UserRepository,
    address_repository: AddressRepository,
    ):
        self.user_repository = user_repository
        self.address_repository = address_repository

    async def __call__(self, user_id: UUID):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        address = self.address_repository.get_by_user_id(user_id)
        if not address:
            raise AddressNotFoundException(f"Address for user ID {user_id} not found")
        return address
