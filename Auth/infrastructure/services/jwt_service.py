from domain.interface.services.jwt_service import JWTServiceInterface
from application.dtos.jwt_token_dto import JWTTokens
from application.interface.security.jwt_security import JWTSecurityInterface
from infrastructure.exceptions import InvalidTokenException
from jwt.exceptions import InvalidTokenError
from config import config_manager
from datetime import timedelta


class JWTService(JWTServiceInterface):
    def __init__(self, jwt_security: JWTSecurityInterface):
        self.jwt_security = jwt_security
    
    async def _create_token(self, payload: dict, token_type: str, expire_timedelta: timedelta):
        """ Генерует токен для пользователя """
        payload.update(type=token_type)
        return self.jwt_security.encode_jwt(payload=payload, expire_timedelta=expire_timedelta)

    async def _decode_token(self, jwt_token: str):
        """ Декодитует токен """
        token_data = self.jwt_security.decode_jwt(jwt_token)
        return token_data
    
    async def create_access_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt_settings.access_token_type,
        expire_time_in_minutes: int = config_manager.jwt_settings.access_token_expire_time_minute,
    ):
        """ Генерует access токен для пользователя """
        expire_timedelta = timedelta(minutes=expire_time_in_minutes)
        return await self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    async def create_refresh_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt_settings.refresh_token_type,
        expire_time_in_days: int = config_manager.jwt_settings.refresh_token_expire_time_day
    ):
        """ Генерует refresh токен для пользователя """
        expire_timedelta = timedelta(days=expire_time_in_days)
        return await self._create_token(payload=payload, token_type=token_type, expire_timedelta=expire_timedelta)
    
    async def generate_jwt_tokens(self, subject: str):
        payload = {"sub":subject}
        access_token = await self.create_access_token(payload)
        refresh_token = await self.create_refresh_token(payload)
        return JWTTokens(access_token=access_token, refresh_token=refresh_token)
    
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
            