from domain.interface.uow.base_uow import BaseUnitOfWork
from domain.interface.services.auth_service import AuthServiceInterface
from domain.entities.user import User
from domain.valueobject.username import Username
from domain.valueobject.email import Email
from domain.valueobject.role import Role
from domain.interface.services.jwt_service import JWTServiceInterface
from application.dtos.jwt_token_dto import JWTTokens
from application.interface.security.password_security import PasswordSecurityInterface
from application.exceptions import AlreadyExistsException, AuthenticationException, UserNotFoundException
from datetime import timedelta


class AuthService(AuthServiceInterface):
    """Сервис для управления регистрацией и аутентификацией пользователей."""
    def __init__(
        self, 
        uow: BaseUnitOfWork,
        password_security: PasswordSecurityInterface,
        jwt_service:JWTServiceInterface,
    ):
        self.uow = uow
        self.password_security = password_security
        self.jwt_service = jwt_service
    
    async def create_user(self, user: User):
        async with self.uow:
            await self.uow.repository.create(user)
            await self.uow.commit()
    
    async def existing_username_and_email(self, username: str, email: str) -> str:
        async with self.uow:
            if await self.uow.repository.find_by_username(username):
                raise AlreadyExistsException("Username already exception")
            if await self.uow.repository.find_by_email(email):
                raise AlreadyExistsException("Email already exception")
        return None

    async def verify_user_credentials(self, username: str, password: bytes):
        async with self.uow:
            existing_user = await self.uow.repository.find_by_username(username)
            if not existing_user:
                raise AuthenticationException("User not found")
            if not self.password_security.verify_password(password, existing_user.hashed_password):
                raise AuthenticationException("Password was not correct")
            return existing_user
    
    async def get_user_data(self, username: str):
        async with self.uow:
            user = await self.uow.repository.find_by_username(username)
            if user is None:
                raise UserNotFoundException("User not found or invalid credentials")
            return user
