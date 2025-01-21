from domain.interface.uow.base_uow import BaseUnitOfWork
from domain.interface.services.auth_service import AuthServiceInterface
from domain.entities.user import User
from domain.valueobject.username import Username
from domain.valueobject.email import Email
from domain.valueobject.role import Role
from application.interface.jwt_security import JWTSecurityInterface
from application.interface.password_security import PasswordSecurityInterface
from application.dtos.jwt_token_dto import JWTTokens
from datetime import timedelta


class AuthService(AuthServiceInterface):
    """Сервис для управления регистрацией и аутентификацией пользователей."""
    def __init__(
        self, 
        uow: BaseUnitOfWork,
        password_service: PasswordSecurityInterface,
        jwt_service: JWTSecurityInterface,
    ):
        self.uow = uow
        self.password_service = password_service
        self.jwt_service = jwt_service
            
    async def register_user(self, username: str, role: str, email: str, password: str):
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        async with self.uow:
            is_user = await self.uow.repository.find_by_username(username)
            is_email = await self.uow.repository.find_by_email(email)
            
            if is_user and is_email:
                raise ValueError("Username or email already exist")
            
            username_vo = Username(username)
            email_vo = Email(email)
            role_vo = Role(role)
            hash_password = self.password_service.get_hash_password(password)
            new_user = User(
                username=username_vo,
                role=role_vo, 
                email=email_vo, 
                password_hash=hash_password
            )
            await self.uow.auth_repository.create(new_user)
            await self.uow.commit(new_user)
    
    async def login_user(self, username: str, password: str):
        """
        Логин пользователя. Проверяет правильность имени пользователя и пароля а так же создает токены.
        """
        async with self.uow:
            user = await self.uow.repository.find_by_username(username)
            
            if not user:
                raise ValueError("Username or password not correct")
            if not self.password_service.verify_password(password, user.hash_password):
                raise ValueError("Username or password not correct")
            
            payload = {"sub": username}
            access_token = await self.create_access_token(payload=payload)
            refresh_token = await self.create_refresh_token(payload=payload)
            return JWTTokens(access_token=access_token, refresh_token=refresh_token)
        
    async def create_access_token(self, payload: dict, expire_time: int | float = 15):
        """ Генерует access токен для пользователя """
        payload.update(type="access")
        access_token = self.jwt_service.encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(minutes=expire_time),
        )
        return access_token
    
    async def create_refresh_token(self, payload: dict, expire_time: int | float = 20):
        """ Генерует refresh токен для пользователя """
        payload.update(type="refresh")
        refresh_token = self.jwt_service.encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(days=expire_time)
        )
        return refresh_token
