from domain.abstacts.uow.base_uow import BaseUnitOfWork
from domain.abstacts.services.auth_service import AuthServiceInterface
from domain.services.password_service import PasswordSecurityService
from domain.entities.user import User
from domain.valueobject.username import Username
from domain.valueobject.email import Email
from domain.valueobject.role import Role



class AuthService(AuthServiceInterface):
    """Сервис для управления регистрацией и аутентификацией пользователей."""
    def __init__(self, uow: BaseUnitOfWork, password_service: PasswordSecurityService):
        self.uow = uow
        self.password_service = password_service
    
    async def register_user(self, username: str, role: str, email: str, password: str):
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        async with self.uow:
            if await self.uow.auth_repository.find_by_username(username):
                raise ValueError("Username already exist")
            
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
        Логин пользователя. Проверяет правильность имени пользователя и пароля.
        """
        async with self.uow:
            user = await self.uow.auth_repository.find_by_username(username)
            if not user and not self.password_service.verify_password(user.password_hash, password):
                raise ValueError("Username or password incorrect")
            return user
    

