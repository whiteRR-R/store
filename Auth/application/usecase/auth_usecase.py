from domain.interface.services.auth_service import AuthServiceInterface
from domain.interface.services.jwt_service import JWTServiceInterface
from domain.interface.usecases.auth_use_case import AuthUseCaseInterface
from domain.entities.user import User
from application.interface.security.password_security import PasswordSecurityInterface
from application.exceptions import (
    AlreadyExistsException,
    AuthenticationException,
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
        password_security: PasswordSecurityInterface
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service
        self.password_security = password_security
    
    async def register(self, username: str, role: str, email: str, password: bytes):
        """
        Регистрация нового пользователя. Проверяет, существует ли уже пользователь с таким именем, 
        и если нет, создает нового пользователя.
        """
        try:
            user_exist = await self.auth_service.existing_username_and_email(username, email)
            if user_exist is None:
                hashed_password = self.password_security.get_hash_password(password)
                user = User.create(username=username,role=role,email=email, hash_password=hashed_password)
                await self.auth_service.create_user(user)
        except AlreadyExistsException as exception:
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
        except AuthenticationException as exception:
            raise AuthenticationException(f"Authentication failed: {str(exception)}")
            
    async def get_current_user_info(self, jwt_token: str):
        """ Возврашает информацию текущего пользователя """
        try:
            is_valid = await self.jwt_service.validate_token_type(
                jwt_token=jwt_token,
                token_type=config_manager.jwt_settings.access_token_type
            )
            if is_valid:
                subject_name = await self.jwt_service.get_token_subject(jwt_token)
                user = await self.auth_service.get_user_data(subject_name)    
                return user
        except AuthenticationException:
            raise UserNotFoundException("Authentication failed: User not found")
    
    async def generate_access_token_from_refresh(self, jwt_token: str):
        """ Генерирует новый access-токен на основе валидного refresh-токена. """
        try:
            is_valid = await self.jwt_service.validate_token_type(
                jwt_token=jwt_token, 
                token_type=config_manager.jwt_settings.refresh_token_type
            )
            
            if is_valid:
                subject = await self.jwt_service.get_token_subject(jwt_token)
                payload = {"sub": subject}
                access_token = await self.jwt_service.create_access_token(payload)
            return access_token
        except Exception:
            raise TokenProcessingException("Failed to generate access token from refresh token")