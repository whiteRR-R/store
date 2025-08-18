from application.dtos.user_dto import UserDTO
from application.exceptions import UsernameAlreadyExistsException, EmailAlreadyExistsException
from application.factories.user_factory import UserFactory
from application.interfaces.security.password_security import PasswordSecurityProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.transaction_manager.transaction_manager import TransactionManager


class RegisterUserInteractor:
    def __init__(self, 
    auth_repository: AuthRepositoryProtocol, 
    password_security: PasswordSecurityProtocol,
    transaction_manager: TransactionManager
    ):
        self.auth_repository = auth_repository
        self.password_security = password_security
        self.transaction_manager = transaction_manager

    async def __call__(self, user_data: UserDTO):
        if await self.auth_repository.get_by_username(user_data.username):
            raise UsernameAlreadyExistsException(user_data.username)
        if await self.auth_repository.get_by_email(user_data.email):
            raise EmailAlreadyExistsException(user_data.email)

        hashed_password = self.password_security.get_hash_password(user_data.password.encode())
        user = UserFactory.create(user_data.username, user_data.role, user_data.email, hashed_password)
        await self.auth_repository.add(user)
        await self.transaction_manager.commit()
