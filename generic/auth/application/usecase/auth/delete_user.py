from config import config_manager
from application.dtos.jwt_token_dto import JWTTokensDTO
from application.exceptions import UserNotFoundException, TokenProcessingException
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol
from domain.interface.transaction_manager.transaction_manager import TransactionManager


class DeleteUserInteractor:
    def __init__(
        self, 
        auth_repository: AuthRepositoryProtocol, 
        redis_repository: RedisRepositoryProtocol, 
        jwt_service: JWTServiceProtocol,
        transaction_manager: TransactionManager
    ):
        self.auth_repository = auth_repository
        self.redis_repository = redis_repository
        self.jwt_service = jwt_service
        self.transaction_manager = transaction_manager

    async def execute(self, jwt_tokens_dto: JWTTokensDTO):
        try:
            self.jwt_service.validate_token_type(jwt_tokens_dto.access_token, config_manager.jwt.ACCESS_TOKEN_TYPE)
            username = self.jwt_service.get_token_subject(jwt_tokens_dto.access_token)
            user = await self.auth_repository.get_by_username(username)

            token_data = self.jwt_service.decode_token(jwt_tokens_dto.refresh_token)
            jti = token_data.get("jti")

            if not user:
                raise UserNotFoundException(username)
            if not await self.redis_repository.exists(f"refresh_token:{jti}"):
                raise TokenProcessingException("Refresh token not found in Redis")

            await self.auth_repository.delete(user)
            await self.transaction_manager.commit()
            await self.redis_repository.delete(f"refresh_token:{jti}")
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid access token: {str(e)}")
