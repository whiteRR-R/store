from config import config_manager
from application.exceptions import TokenProcessingException
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol


class LogoutUserInteractor:
    def __init__(self, redis_repository: RedisRepositoryProtocol, jwt_service: JWTServiceProtocol):
        self.redis_repository = redis_repository
        self.jwt_service = jwt_service

    async def execute(self, access_token: str, refresh_token: str):
        try:
            self.jwt_service.validate_token_type(access_token, config_manager.jwt.ACCESS_TOKEN_TYPE)
            token_data = self.jwt_service.decode_token(refresh_token)
            jti = token_data.get("jti")
            if not await self.redis_repository.exists(f"refresh_token:{jti}"):
                raise TokenProcessingException("Refresh token not found in Redis")
            await self.redis_repository.delete(f"refresh_token:{jti}")
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid token: {str(e)}")
