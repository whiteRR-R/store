from domain.interface.uow.base_uow import BaseUnitOfWork
from domain.interface.services.auth_service import AuthServiceInterface
from domain.entities.user import User
from domain.valueobject.username import Username
from domain.valueobject.email import Email
from domain.valueobject.role import Role
from domain.interface.services.jwt_service import JWTServiceInterface
from application.dtos.jwt_token_dto import JWTTokens
from application.interface.security.password_security import PasswordSecurityInterface
from application.exceptions import AlreadyExistsException, AuthException, UserNotFoundException
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
        user = self.uow.repository.create(user)
        await self.uow.register_new(user)
        await self.uow.commit()
    
    async def existing_username_and_email(self, username: str, email: str) -> str:
        if await self.uow.repository.find_by_username(username):
            raise AlreadyExistsException("Username already exception")
        if await self.uow.repository.find_by_email(email):
            raise AlreadyExistsException("Email already exception")
        return None

    async def verify_user_credentials(self, username: str, password: bytes):
        existing_user = await self.uow.repository.find_by_username(username)
        if not existing_user:
            raise AuthException("User not found")
        if not self.password_security.verify_password(password, existing_user.hashed_password):
            raise AuthException("Password was not correct")
        return existing_user
    
    async def get_user_by_username(self, username: str):
        user = await self.uow.repository.find_by_username(username)
        if user is None:
            raise UserNotFoundException("User not found or invalid credentials")
        return user
     
    async def get_user_by_email(self, email: str):
        user = await self.uow.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundException("User not found or invalid credentials")
        return user
    
    async def update_password(self, username: str, new_password: bytes):
        user = await self.get_user_by_username(username)
        hashed_password = self.password_security.get_hash_password(new_password)
        updated_user = User.create(username=user.username,role=user.role,email=user.email, hash_password=hashed_password)
        await self.uow.register_dirty(updated_user)
        await self.commit()
            
        
