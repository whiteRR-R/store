from uuid import UUID
from application.dtos.user import UserDTO
from application.factories.user_factory import UserFactory
from application.exceptions import UserNotFoundException
from domain.interfaces.repositories.user_repository import UserRepository


class GetUserByIDUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> UserDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")
        return UserFactory.to_dto(user)
