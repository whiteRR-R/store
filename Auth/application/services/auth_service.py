from domain.interface.uow.base_uow import BaseUnitOfWork
from domain.interface.services.auth_service import AuthServiceInterface
from domain.entities.user import User
from domain.valueobject.username import Username
from domain.valueobject.email import Email
from domain.valueobject.role import Role
from domain.interface.services.jwt_service import JWTServiceInterface
from application.interface.security.password_security import PasswordSecurityInterface
from application.dtos.jwt_token_dto import JWTTokens
from application.exceptions import AlreadyExistsException, AuthenticationException, UserNotFoundException, InvalidTokenException
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
            
    async def register_user(self, username: str, role: str, email: str, password: bytes):
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        async with self.uow:
            existing_user = await self.uow.repository.find_by_username(username)
            existing_email = await self.uow.repository.find_by_email(email)
            
            if existing_user or existing_email:
                raise ValueError("Username or email already exist")
            
            username_value = Username(username)
            email_value = Email(email)
            role_value = Role(role)
            hash_password = self.password_security.get_hash_password(password)
            new_user = User(
                username=username_value,
                role=role_value, 
                email=email_value, 
                hash_password=hash_password
            )
            await self.uow.repository.create(new_user)
            await self.uow.commit()
    
    async def login_user(self, username: str, password: bytes):
        """
        Логин пользователя. Проверяет правильность имени пользователя и пароля а так же создает токены.
        """
        async with self.uow:
            user = await self.uow.repository.find_by_username(username)
            
            if not user:
                raise AuthenticationException("Username or password not correct")
            if not self.password_security.verify_password(password, user.hashed_password):
                raise AuthenticationException("Username or password not correct")
            
            payload = {"sub": username}
            access_token = await self.jwt_service.create_access_token(payload)
            refresh_token = await self.jwt_service.create_refresh_token(payload)
            return JWTTokens(access_token=access_token, refresh_token=refresh_token)
    
    async def get_current_user_info(self, jwt_token: str):
        """ Возврашает информацию текущего пользователя """
        async with self.uow:
            subject_name = self.jwt_service.get_token_subject(jwt_token)
            user = self.uow.repository.find_by_username(subject_name)
            
            if user is None:
                raise UserNotFoundException("User not found or invalid credentials")
            
            return user
                
    
