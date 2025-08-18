from application.dtos.login_dto import UserLoginDTO
from application.exceptions import InvalidCredentialsException
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from application.interface.security.password_security import PasswordSecurityProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol


class LoginUserInteractor:
    def __init__(
        self,
        auth_repository: AuthRepositoryProtocol,
        redis_repository: RedisRepositoryProtocol,
        password_security: PasswordSecurityProtocol,
        jwt_service: JWTServiceProtocol,
    ):
        self.auth_repository = auth_repository
        self.redis_repository = redis_repository
        self.password_security = password_security
        self.jwt_service = jwt_service

    async def __call__(self, user_credentials: UserLoginDTO):
        user = await self.auth_repository.get_by_username(user_credentials.username)
        if not user:
            raise InvalidCredentialsException()
        if not self.password_security.verify_password(user_credentials.password.encode(), user.hash_password):
            raise InvalidCredentialsException()

        jwt_tokens = self.jwt_service.generate_jwt_tokens(user.username)
        refresh_token = self.jwt_service.decode_token(jwt_tokens.refresh_token)
        refresh_jti = refresh_token.get("jti")
        await self.redis_repository.set(f"refresh_token:{refresh_jti}", jwt_tokens.refresh_token)
        return jwt_tokens
