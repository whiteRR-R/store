from config import config_manager
from application.exceptions import UserNotFoundException, TokenProcessingException
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from application.interfaces.security.token_provider import TokenProviderProtocol


class GetCurrentUserInfoInteractor:
    def __init__(self, auth_repository: AuthRepositoryProtocol, jwt_service: TokenProviderProtocol):
        self.auth_repository = auth_repository
        self.jwt_service = jwt_service

    async def __call__(self, jwt_token: str):
        try:
            self.jwt_service.validate_token_type(jwt_token, config_manager.jwt.ACCESS_TOKEN_TYPE)
            username = self.jwt_service.get_token_subject(jwt_token)
            user = await self.auth_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(username)
            return user
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid access token: {str(e)}")
