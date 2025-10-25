from domain.interfaces.repositories.user_repository import UserRepository
from domain.interfaces.repositories.outbox_repository import OutboxRepository
from application.dtos.user import UserCreateDTO, UserDTO
from application.factories.user_factory import UserFactory
from application.interfaces.transaction_manager import TransactionManager


class UserCreateUseCase:
    def __init__(
        self, 
        user_repository: UserRepository,
        outbox_repository: OutboxRepository,
        transaction_manager: TransactionManager
    ):
        self.user_repository = user_repository
        self.outbox_repository = outbox_repository
        self.transaction_manager = transaction_manager
    
    async def __call__(self, user_dto: UserCreateDTO) -> UserDTO:
        user = UserFactory.from_dto(user_dto)
        await self.user_repository.add(user)
        # await self.outbox_repository.add()
        await self.transaction_manager.commit()
        return UserFactory.to_dto(user)
