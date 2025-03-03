from domain.entities.user import User
from domain.interface.uow.base_uow import BaseUnitOfWork
from domain.interface.services.auth_service import AuthServiceInterface
from domain.interface.services.jwt_service import JWTServiceInterface
from domain.interface.repository.auth_repository import AuthRepositoryInterface
from application.dtos.login_dto import UserLoginDTO
from application.dtos.user_dto import UserDTO
from application.dtos.reset_password_dto import ResetPasswordDTO
from application.helpers.dtos import user_dto_to_user_entity
from application.interface.security.password_security import PasswordSecurityInterface
from application.exceptions import AlreadyExistsException, AuthException, UserNotFoundException
from typing import Optional


class AuthService(AuthServiceInterface):
    """Сервис для управления регистрацией и аутентификацией пользователей."""
    def __init__(
        self, 
        unit_of_work: BaseUnitOfWork,
        auth_repository: AuthRepositoryInterface,
        password_security: PasswordSecurityInterface,
        jwt_service:JWTServiceInterface,
    ):
        self.unit_of_work = unit_of_work 
        self.auth_repository = auth_repository
        self.password_security = password_security
        self.jwt_service = jwt_service
    
    async def create_user(self, user_dto: UserDTO):
        """Создает нового пользователя, предварительно проверяя существует ли такой пользователь."""
        await self._existing_username_or_email(username=user_dto.username, email=user_dto.email)
        hashed_password = self.password_security.get_hash_password(user_dto.password)
        updated_user_dto = UserDTO(
            username=user_dto.username,
            email=user_dto.email,
            password=hashed_password,
            role=user_dto.role
        )
        new_user = user_dto_to_user_entity(updated_user_dto)
        await self.unit_of_work.register_new(new_user)
        await self.unit_of_work.commit()

    async def verify_user_credentials(self, user_credentials: UserLoginDTO) -> User:
        """Проверяет учетные данные пользователя."""
        existing_user = await self.auth_repository.find_by_username(user_credentials.username)
        password_bytes = user_credentials.password.encode()
        if not existing_user:
            raise AuthException("User not found")
        if not self.password_security.verify_password(password_bytes, existing_user.hashed_password):
            raise AuthException("Password was not correct")
        return existing_user
    
    async def _existing_username_or_email(self, username: str, email: str) -> str:
        """Проверяет, существует ли уже пользователь с таким username или email."""
        if await self.auth_repository.find_by_username(username):
            raise AlreadyExistsException("Username already exception")
        if await self.auth_repository.find_by_email(email):
            raise AlreadyExistsException("Email already exception")
        return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Получает пользователя по username или вызывает исключение."""
        user = await self.auth_repository.find_by_username(username)
        if user is None:
            raise UserNotFoundException("User not found or invalid credentials")
        return user
     
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получает пользователя по email или вызывает исключение."""
        user = await self.auth_repository.find_by_email(email)
        if user is None:
            raise UserNotFoundException("User not found or invalid credentials")
        return user

    async def update_password(self, username: str, new_password: bytes):
        """Обновляет пароль пользователя."""
        user = await self.get_user_by_username(username)
        hashed_password = self.password_security.get_hash_password(new_password)
        user.update_password(hashed_password)
        await self.unit_of_work.register_dirty(user)
        await self.unit_of_work.commit()
