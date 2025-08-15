from uuid import UUID
from application.factories.user_factory import UserFactory
from domain.interfaces.repositories.user_repository import UserRepository
from domain.interfaces.transaction_manager import TransactionManager
from application.dtos.user import UserEmailUpdateDTO
from application.exceptions import UserNotFoundException


class UpdateUserEmailUseCase:
    def __init__(self, user_repository: UserRepository, transaction_manager: TransactionManager):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager
        
    async def __call__(self, user_id: UUID, update_user_dto: UserEmailUpdateDTO):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        user.change_email(update_user_dto.email)
        await self.user_repository.update(user)
        await self.transaction_manager.commit()
        return UserFactory.to_dto(user)
