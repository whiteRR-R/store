from domain.interface.services.auth_service import AuthServiceInterface
from domain.interface.services.jwt_service import JWTServiceInterface
from domain.interface.usecases.auth_usecase import AuthUseCaseInterface
from domain.entities.user import User
from application.interface.security.password_security import PasswordSecurityInterface
from application.exceptions import (
    ApplicationException,
    AuthException,
    UserNotFoundException,
    RegistrationException,
    TokenProcessingException,
)
from config import config_manager


class AuthUseCase(AuthUseCaseInterface):
    def __init__(
        self,
        auth_service: AuthServiceInterface,
        jwt_service: JWTServiceInterface,
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service
    
    async def register(self, username: str, role: str, email: str, password: bytes):
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        try:
            await self.auth_service.existing_username_and_email(username, email)
            hashed_password = self.password_security.get_hash_password(password)
            user = User.create(username=username,role=role,email=email, hash_password=hashed_password)
            await self.auth_service.create_user(user)
        except RegistrationException as exception:
            raise RegistrationException(f"Registration failed: {str(exception)}")
        
    async def login(self, username: str, password: str):
        """
        Логин пользователя. Проверяет правильность имени пользователя и пароля а так же создает токены.
        """
        try: 
            password_bytes = password.encode()
            user = await self.auth_service.verify_user_credentials(username, password_bytes)
            jwt_tokens = await self.jwt_service.generate_jwt_tokens(user.username)
            return jwt_tokens
        except AuthException as exception:
            raise AuthException(f"Authentication failed: {str(exception)}")
            
    async def get_current_user_info(self, jwt_token: str):
        """ Возврашает информацию текущего пользователя """
        try:
            await self.jwt_service.validate_token_type(jwt_token=jwt_token, token_type=config_manager.jwt.RESET_TOKEN_TYPE)
            subject_name = await self.jwt_service.get_token_subject(jwt_token)
            user = await self.auth_service.get_user_by_username(subject_name)    
            return user
        except AuthException as exception:
            raise UserNotFoundException(f"User not found: {str(exception)}")
    
    async def generate_access_token_from_refresh(self, jwt_token: str):
        """ Генерирует новый access-токен на основе валидного refresh-токена. """
        try:
            await self.jwt_service.validate_token_type(jwt_token=jwt_token, token_type=config_manager.jwt.RESET_TOKEN_TYPE)
            subject = await self.jwt_service.get_token_subject(jwt_token)
            payload = {"sub": subject}
            access_token = await self.jwt_service.create_access_token(payload)
            return access_token
        except ApplicationException as exception:
            raise TokenProcessingException(f"Failed to generate access token from refresh token: {str(exception)}")
    
    async def forgot_password(self, email: str):
        """ Генерирует reset-токен для сброса пароля """
        try:
            user = await self.auth_service.get_user_by_email(email)
            payload = {"sub": user.username}
            reset_token = self.jwt_service.create_reset_token(payload)
            #TODO: Добавить отправку ссылку для сброса на почту
            return reset_token
        except UserNotFoundException:
            raise UserNotFoundException("User not found")
        except Exception as exception:
            raise ApplicationException(f"Failed to generate token: {str(exception)}")
    
    async def reset_password(self, jwt_token: str, new_password: bytes):
        """ Сбросывает пароль через reset-токен """
        try:
            await self.jwt_service.validate_token_type(jwt_token=jwt_token, token_type=config_manager.jwt.RESET_TOKEN_TYPE)
            subject = await self.jwt_service.get_token_subject(jwt_token)
            await self.auth_service.update_password(subject, new_password)  
        except UserNotFoundException:
            raise UserNotFoundException("User not found for password reset.")
        except Exception as exception:
            raise ApplicationException(f"Unexpected error during password reset: {str(exception)}")      
