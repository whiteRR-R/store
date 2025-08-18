from application.dtos.jwt_token_dto import JWTTokenDTO
from application.exceptions import TokenProcessingException
from config import config_manager
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol


class GenerateAccessTokenFromRefreshInteractor:
    def __init__(self, redis_repository: RedisRepositoryProtocol, jwt_service: JWTServiceProtocol):
        self.redis_repository = redis_repository
        self.jwt_service = jwt_service

    async def execute(self, jwt_dto: JWTTokenDTO):
        try:
            self.jwt_service.validate_token_type(jwt_dto.token, config_manager.jwt.REFRESH_TOKEN_TYPE)
            token_data = self.jwt_service.decode_token(jwt_dto.token)
            jti = token_data.get("jti")

            if not await self.redis_repository.exists(f"refresh_token:{jti}"):
                raise TokenProcessingException("Refresh token not found in Redis")

            username = self.jwt_service.get_token_subject(jwt_dto.token)
            return self.jwt_service.create_access_token({"sub": username})
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Failed to generate access token: {str(e)}")
