from config import config_manager
from domain.valueobject.email import Email
from domain.factories.user_factory import UserFactory
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol
from application.interface.security.password_security import PasswordSecurityProtocol
from application.dtos.user_dto import UserDTO
from application.dtos.login_dto import UserLoginDTO
from application.dtos.jwt_token_dto import JWTTokenDTO
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
        password_security: PasswordSecurityProtocol,
        jwt_service: JWTServiceProtocol,
    ):
        self.auth_repository = auth_repository
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
        return self.jwt_service.generate_jwt_tokens(user.username)

    async def delete(self, jwt_token: str):
        """ Удаляет пользователя по JWT токену """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=jwt_token,
                token_type=config_manager.jwt.ACCESS_TOKEN_TYPE
            )
            username = self.jwt_service.get_token_subject(jwt_token)
            user = await self.auth_repository.get_by_username(username)
            if not user:
                raise UserNotFoundException(username)
            await self.auth_repository.delete(user)
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid access token: {str(e)}")

    async def forgot_password(self, forgot_dto: ForgotPasswordDTO):
        """ Генерирует токен для сброса пароля """
        user = await self.auth_repository.get_by_email(forgot_dto.email)
        if not user:
            raise UserNotFoundException(f"User with email '{forgot_dto.email}' not found.")
        return self.jwt_service.create_reset_token({"sub": user.username})

    async def reset_password(self, reset_dto: ResetPasswordDTO):
        """ Сбрасывает пароль пользователя по токену сброса """
        try:
            self.jwt_service.validate_token_type(
                jwt_token=reset_dto.reset_token,
                token_type=config_manager.jwt.RESET_TOKEN_TYPE
            )
            username = self.jwt_service.get_token_subject(reset_dto.reset_token)
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
            user.update_email(new_email)
            await self.auth_repository.update(user)
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Invalid reset token: {str(e)}")

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
            username = self.jwt_service.get_token_subject(jwt_dto.token)
            return self.jwt_service.create_access_token(username)
        except TokenProcessingException as e:
            raise TokenProcessingException(f"Failed to generate access token: {str(e)}")
