from application.dtos.jwt_token_dto import JWTTokensDTO
from application.interface.security.jwt_security import JWTSecurityProtocol
from infrastructure.exceptions import InvalidTokenException, InvalidTokenTypeException
from jwt.exceptions import InvalidTokenError
from config import config_manager
from datetime import timedelta


class JWTService:
    """ Сервис для работы с JWT токенами """
    def __init__(self, jwt_security: JWTSecurityProtocol):
        self.jwt_security = jwt_security
    
    async def _create_token(self, payload: dict, token_type: str, expire_timedelta: timedelta):
        """ Генерует токен для пользователя """
        payload.update(type=token_type)
        return self.jwt_security.encode_jwt(payload=payload, expire_timedelta=expire_timedelta)

    async def _decode_token(self, jwt_token: str):
        """ Декодитует токен """
        token_data = self.jwt_security.decode_jwt(jwt_token)
        return token_data
    
    async def create_reset_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.RESET_TOKEN_TYPE,
        expire_time_in_minutes = config_manager.jwt.reset_token_expire_time_minute,
    ):
        """ Генерует reset токен для пользователя для зброса пароля """
        expire_timedelta = timedelta(minutes=expire_time_in_minutes)
        return await self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    async def create_access_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.ACCESS_TOKEN_TYPE,
        expire_time_in_minutes: int = config_manager.jwt.access_token_expire_time_minute,
    ):
        """ Генерует access токен для пользователя """
        expire_timedelta = timedelta(minutes=expire_time_in_minutes)
        return await self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    async def create_refresh_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.REFRESH_TOKEN_TYPE,
        expire_time_in_days: int = config_manager.jwt.refresh_token_expire_time_day
    ):
        """ Генерует refresh токен для пользователя """
        expire_timedelta = timedelta(days=expire_time_in_days)
        return await self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    async def generate_jwt_tokens(self, subject: str):
        """ Генерует refresh и access токены и возвращает их"""
        payload = {"sub":subject}
        access_token = await self.create_access_token(payload)
        refresh_token = await self.create_refresh_token(payload)
        return JWTTokensDTO(access_token=access_token, refresh_token=refresh_token)
    
    async def validate_token_type(self, jwt_token: str, token_type: str):
        """ Проверяет, соответствует ли тип токена ожидаемому, и возвращает subject токена. """
        jwt_data = await self._decode_token(jwt_token)
        jwt_type = jwt_data.get("type")
        if jwt_type != token_type:
            raise InvalidTokenTypeException(f"Invalid token type {jwt_type!r} excepted {token_type!r}")
        return True
    
    async def get_token_subject(self, jwt_token: str):
        """ Возвращает имя пользователя из токена """
        try:
            token_data = await self._decode_token(jwt_token)
            subject = token_data.get("sub")
            if subject is None:
                raise InvalidTokenException("Could not validate credentials")
            return subject
        except InvalidTokenError:
                raise InvalidTokenException("Could not validate credentials")
            