import uuid
from datetime import timedelta, datetime, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from application.dtos.jwt_token_dto import JWTTokensDTO
from infrastructure.exceptions import InvalidTokenException, InvalidTokenTypeException
from config import config_manager


class JWTService:
    """ Сервис для работы с JWT токенами """
    def __init__(self):
        self._private_key: str = config_manager.jwt.PRIVATE_KEY.read_text()
        self._public_key: str = config_manager.jwt.PUBLIC_KEY.read_text()
        self._algorithm: str = config_manager.jwt.ALGORITHM
        
    def _create_token(
        self,
        payload: dict,
        token_type: str,
        expire_timedelta: timedelta | None = None,
        ):
        """Кодирует JWT токен"""
        
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        
        if expire_timedelta:
            expire_time = now + expire_timedelta
        else:
            expire_time = now + timedelta(minutes=15)
        
        to_encode.update(
            iat=now,
            exp=expire_time,
            type=token_type,
            jti=uuid.uuid4().hex
        )
        encoded = jwt.encode(payload=to_encode, key=self._private_key, algorithm=self._algorithm)
        return encoded
    
    def decode_token(
        self,
        jwt_token: str,
        ):
        """Декодирует JWT токен"""  
        decoded = jwt.decode(jwt=jwt_token, key=self._public_key, algorithms=[self._algorithm])
        return decoded
    
    def validate_token_type(self, jwt_token: str, token_type: str):
        """ Проверяет, соответствует ли тип токена ожидаемому, и возвращает subject токена. """
        jwt_data = self.decode_token(jwt_token)
        jwt_type = jwt_data.get("type")
        if jwt_type != token_type:
            raise InvalidTokenTypeException(f"Invalid token type {jwt_type!r} excepted {token_type!r}")
        return None
    
    def create_reset_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.RESET_TOKEN_TYPE,
        expire_time_in_minutes = config_manager.jwt.reset_token_expire_time_minute,
    ):
        """ Генерует reset токен для пользователя для зброса пароля """
        expire_timedelta = timedelta(minutes=expire_time_in_minutes)
        return self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    def create_access_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.ACCESS_TOKEN_TYPE,
        expire_time_in_minutes: int = config_manager.jwt.access_token_expire_time_minute,
    ):
        """ Генерует access токен для пользователя """
        expire_timedelta = timedelta(minutes=expire_time_in_minutes)
        return self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    def create_refresh_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.REFRESH_TOKEN_TYPE,
        expire_time_in_days: int = config_manager.jwt.refresh_token_expire_time_day
    ):
        """ Генерует refresh токен для пользователя """
        expire_timedelta = timedelta(days=expire_time_in_days)
        return self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    def generate_jwt_tokens(self, subject: str):
        payload = {"sub":subject}
        access_token = self.create_access_token(payload)
        refresh_token = self.create_refresh_token(payload)
        return JWTTokensDTO(access_token=access_token, refresh_token=refresh_token)
    
    def get_token_subject(self, jwt_token: str) -> str:
        """ Возвращает имя пользователя из токена """
        try:
            token_data = self.decode_token(jwt_token)
            return token_data.get("sub")
        except InvalidTokenError:
            raise InvalidTokenException("Could not validate credentials")
            