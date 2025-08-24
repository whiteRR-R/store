from config import config_manager
from application.dtos.jwt_token_dto import JWTTokenDTO
from application.exceptions import UserNotFoundException, TokenProcessingException
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from application.interfaces.security.token_provider import TokenProviderProtocol
from application.interfaces.transaction_manager import TransactionManagerProtocol


class DeleteUserInteractor:
    def __init__(
        self, 
        auth_repository: AuthRepositoryProtocol, 
        redis_repository: RedisRepositoryProtocol, 
        jwt_service: TokenProviderProtocol,
        transaction_manager: TransactionManagerProtocol
    ):
        self.auth_repository = auth_repository
        self.redis_repository = redis_repository
        self.jwt_service = jwt_service
        self.transaction_manager = transaction_manager

    async def __call__(self, jwt_token_dto: JWTTokenDTO):
        try:
            self.jwt_service.validate_token_type(jwt_token_dto.token, config_manager.jwt.ACCESS_TOKEN_TYPE)
            username = self.jwt_service.get_token_subject(jwt_token_dto.token)
            user = await self.auth_repository.get_by_username(username)
            await self.auth_repository.delete(user)
            await self.transaction_manager.commit()
        except TokenProcessingException:
            raise TokenProcessingException(f"Invalid access token: {jwt_token_dto.token}")
