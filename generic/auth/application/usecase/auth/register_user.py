from application.dtos.user_dto import UserDTO, UserGatewayDTO
from application.exceptions import ApplicationException, UsernameAlreadyExistsException, EmailAlreadyExistsException
from application.factories.user_factory import UserFactory
from application.interfaces.gateways.user_gateway import UserGateway
from domain.interface.services.hash_service import PasswordHasherProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.transaction_manager.transaction_manager import TransactionManagerProtocol
import logging


logger = logging.getLogger(__name__)

class RegisterUserInteractor:
    def __init__(self, 
    auth_repository: AuthRepositoryProtocol, 
    password_hasher: PasswordHasherProtocol,
    transaction_manager: TransactionManagerProtocol,
    user_gateway: UserGateway,
    ):
        self.auth_repository = auth_repository
        self.password_hasher = password_hasher
        self.transaction_manager = transaction_manager
        self.user_gateway = user_gateway

    async def __call__(self, user_dto: UserDTO):
        try:
            if await self.auth_repository.get_by_username(user_dto.username):
                raise UsernameAlreadyExistsException(user_dto.username)
            if await self.auth_repository.get_by_email(user_dto.email):
                raise EmailAlreadyExistsException(user_dto.email)

            hashed_password = self.password_hasher.hash(user_dto.password)
            user = UserFactory.from_dto(user_dto, hashed_password)
            user_gateway_dto = UserFactory.to_gateway_dto(user)
            print(user_gateway_dto)
            await self.user_gateway.create_user(user_gateway_dto)
            await self.auth_repository.add(user)
            await self.transaction_manager.commit()
        except ApplicationException as e:
            await self.transaction_manager.rollback()
            raise e
