from uuid import UUID, uuid4
from config import config_manager
from domain.valueobject.email import Email
from domain.valueobject.role import Role
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.repository.redis_repository import RedisRepositoryProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol
from application.factories.user_factory import UserFactory
from application.interface.security.password_security import PasswordSecurityProtocol
from application.dtos.user_dto import UserDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO, JWTTokensDTO
from application.dtos.forgot_password_dto import ForgotPasswordDTO
from application.dtos.reset_password_dto import ResetPasswordDTO
from application.dtos.change_email import ChangeEmailDTO
from application.exceptions import (
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    TokenProcessingException,
)


class AuthUseCase:
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

    async def register(self, user_data: UserDTO):
        """ Регистрация нового пользователя"""
        if await self.auth_repository.get_by_username(user_data.username):
            raise UsernameAlreadyExistsException(user_data.username)
        if await self.auth_repository.get_by_email(user_data.email):
            raise EmailAlreadyExistsException(user_data.email)

        hashed_password = self.password_security.get_hash_password(user_data.password.encode())
        user = UserFactory.create(
            user_data.username,
            user_data.role,
            user_data.email,
            hashed_password
        )
        await self.auth_repository.add(user)

    async def login(self, user_credentials: UserLoginDTO):
        """ Аутентификация пользователя и генерация JWT токенов """
        user = await self.auth_repository.get_by_username(user_credentials.username)
        if not user:
            raise InvalidCredentialsException()
        if not self.password_security.verify_password(user_credentials.password.encode(), user.hash_password):
            raise InvalidCredentialsException()
        jwt_tokens = self.jwt_service.generate_jwt_tokens(user.username)
        refresh_token = self.jwt_service.decode_token(jwt_tokens.refresh_token)
        refresh_jti = refresh_token.get("jti")
        await self.redis_repository.set(
            key=f"refresh_token:{refresh_jti}",
            value=jwt_tokens.refresh_token,
        )
        return jwt_tokens
    
    async def logout(self, access_token: str, refresh_token: str):
        """ Выход пользователя """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=access_token,
                token_type=config_manager.jwt.ACCESS_TOKEN_TYPE
            )
            token_data = self.jwt_service.decode_token(refresh_token)
            jti = token_data.get("jti")
            if not await self.redis_repository.exists(f"refresh_token:{jti}"):
                raise TokenProcessingException("Refresh token not found in Redis")
            await self.redis_repository.delete(f"refresh_token:{jti}")
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid token: {str(e)}")
        
    async def delete(self, jwt_tokens_dto: JWTTokensDTO):
        """ Удаляет пользователя по JWT токену """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=jwt_tokens_dto.access_token,
                token_type=config_manager.jwt.ACCESS_TOKEN_TYPE
            )
            username = self.jwt_service.get_token_subject(jwt_tokens_dto.access_token)
            user = await self.auth_repository.get_by_username(username)
            token_data = self.jwt_service.decode_token(jwt_tokens_dto.refresh_token)
            jti = token_data.get("jti")
            if not user:
                raise UserNotFoundException(username)
            if not await self.redis_repository.exists(f"refresh_token:{jti}"):
                raise TokenProcessingException("Refresh token not found in Redis")
            await self.auth_repository.delete(user)
            await self.redis_repository.delete(f"refresh_token:{jti}")
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid access token: {str(e)}")

    async def forgot_password(self, forgot_dto: ForgotPasswordDTO):
        """ Генерирует токен для сброса пароля """
        user = await self.auth_repository.get_by_email(forgot_dto.email)
        if not user:
            raise UserNotFoundException(f"User with email '{forgot_dto.email}' not found.")
        reset_key = uuid4().hex
        await self.redis_repository.set(key=f"reset_password:{reset_key}", value=user.username)
        return reset_key

    async def reset_password(self, reset_dto: ResetPasswordDTO):
        """ Сбрасывает пароль пользователя по токену сброса """
        try:
            if not await self.redis_repository.exists(f"reset_password:{reset_dto.reset_key}"):
                raise TokenProcessingException("Reset key not found in Redis")
            username = await self.redis_repository.getdel(f"reset_password:{reset_dto.reset_key}")
            user = await self.auth_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(username)
            hashed_password = self.password_security.get_hash_password(reset_dto.new_password.encode())
            user.change_password(hashed_password)
            await self.auth_repository.update(user)
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")

    async def update_email(self, jwt_token: str, dto: ChangeEmailDTO):
        """ Обновляет email пользователя по JWT токену """
        try:
            self.jwt_service.validate_token_type(
                    jwt_token=jwt_token,
                    token_type=config_manager.jwt.ACCESS_TOKEN_TYPE
                )
            username = self.jwt_service.get_token_subject(jwt_token)
            user = await self.auth_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(username)
            if await self.auth_repository.get_by_email(dto.new_email):
                raise EmailAlreadyExistsException(dto.new_email)
            new_email = Email(dto.new_email)
            user.change_email(new_email)
            await self.auth_repository.update(user)
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")
    
    async def update_role(self, user_id: UUID, new_role: Role):
        user = await self.auth_repository.get_by_id(user_id)
        if not user:
            UserNotFoundException(user_id)
        user.change_role(new_role)
        await self.auth_repository.update(user)

    async def get_current_user_info(self, jwt_token: str):
        """ Получает информацию о текущем пользователе по JWT токену """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=jwt_token,
                token_type=config_manager.jwt.ACCESS_TOKEN_TYPE
            )
            username = self.jwt_service.get_token_subject(jwt_token)
            user = await self.auth_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(username)
            return user
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid access token: {str(e)}")

    async def generate_access_token_from_refresh(self, jwt_dto: JWTTokenDTO):
        """ Генерирует новый access token из refresh token """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=jwt_dto.token,
                token_type=config_manager.jwt.REFRESH_TOKEN_TYPE
            )
            token_data = self.jwt_service.decode_token(jwt_dto.token)
            jti = token_data.get("jti")
            if not await self.redis_repository.exists(f"refresh_token:{jti}"):
                raise TokenProcessingException("Refresh token not found in Redis")
            username = self.jwt_service.get_token_subject(jwt_dto.token)
            return self.jwt_service.create_access_token({"sub": username})
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Failed to generate access token: {str(e)}")
