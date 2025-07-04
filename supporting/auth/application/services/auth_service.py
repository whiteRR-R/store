from typing import Optional
from domain.entities.user import User
from domain.interface.uow.base_uow import UnitOfWorkProtocol
from domain.interface.services.jwt_service import JWTServiceProtocol
from domain.interface.repository.auth_repository import AuthRepositoryProtocol
from domain.factories.user_factory import UserFactory
from application.dtos.login_dto import UserLoginDTO
from application.dtos.user_dto import UserDTO
from application.interface.security.password_security import PasswordSecurityProtocol
from application.exceptions import (
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
)


class AuthService:
    """Сервис для управления регистрацией и аутентификацией пользователей."""
    def __init__(
        self, 
        auth_repository: AuthRepositoryProtocol,
        password_security: PasswordSecurityProtocol,
        jwt_service: JWTServiceProtocol,
    ):
        self.auth_repository = auth_repository
        self.password_security = password_security
        self.jwt_service = jwt_service

    async def _existing_username_or_email(self, username: str, email: str) -> None:
        """Проверяет, существует ли уже пользователь с таким username или email."""
        if await self.auth_repository.get_by_username(username):
            raise UsernameAlreadyExistsException(username)
        if await self.auth_repository.get_by_email(email):
            raise EmailAlreadyExistsException(email)
        return None
    
    async def create_user(self, user_dto: UserDTO):
        """Создает нового пользователя, предварительно проверяя существует ли такой пользователь."""
        await self._existing_username_or_email(username=user_dto.username, email=user_dto.email)
        hashed_password = self.password_security.get_hash_password(user_dto.password)
        new_user = UserFactory.create(
            user_dto.username,
            user_dto.role,
            user_dto.email,
            hashed_password
        )
        await self.auth_repository.add(new_user)

    async def verify_user_credentials(self, user_credentials: UserLoginDTO) -> User:
        """Проверяет учетные данные пользователя."""
        existing_user = await self.auth_repository.get_by_username(user_credentials.username)
        if not existing_user:
            raise UserNotFoundException(user_credentials.username)
        if not self.password_security.verify_password(
            user_credentials.password.encode(), 
            existing_user.hash_password
        ):
            raise InvalidCredentialsException()
        return existing_user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Получает пользователя по username или вызывает исключение."""
        user = await self.auth_repository.get_by_username(username)
        if user is None:
            raise UserNotFoundException("User not found or invalid credentials")
        return user
     
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получает пользователя по email или вызывает исключение."""
        user = await self.auth_repository.get_by_email(email)
        if user is None:
            raise UserNotFoundException("User not found or invalid credentials")
        return user

    async def update_password(self, username: str, new_password: bytes):
        """Обновляет пароль пользователя."""
        user = await self.get_user_by_username(username)
        if user is None:
            raise UserNotFoundException(f"User with username '{username}' not found.")
        hashed_password = self.password_security.get_hash_password(new_password)
        user.change_password(hashed_password)
        await self.auth_repository.update(user)

    async def delete_user(self, username: str):
        """Удаляет пользователя по username."""
        user = await self.get_user_by_username(username)
        if user is None:
            raise UserNotFoundException(f"User with username '{username}' not found.")
        await self.auth_repository.delete(user)
