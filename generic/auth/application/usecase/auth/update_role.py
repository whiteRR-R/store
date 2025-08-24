from uuid import UUID
from application.exceptions import UserNotFoundException
from domain.interface.transaction_manager.transaction_manager import TransactionManagerProtocol
from domain.enums.role import Role
from domain.interface.repository.auth_repository import AuthRepositoryProtocol


class UpdateRoleInteractor:
    def __init__(self, auth_repository: AuthRepositoryProtocol, transaction_manager: TransactionManagerProtocol):
        self.auth_repository = auth_repository
        self.transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, new_role: Role):
        user = await self.auth_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        user.change_role(new_role)
        await self.auth_repository.update(user)
        await self.transaction_manager.commit()
