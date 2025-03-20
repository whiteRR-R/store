from typing import Protocol
from datetime import timedelta

class JWTSecurityProtocol(Protocol):
    def encode_jwt(self, payload: dict, expire_timedelta: timedelta | None) -> str:
        """ Генерирует JWT токен """
        pass
    
    def decode_jwt(self, jwt_token: str):
        """ Декодирует JWT токен """
        pass
    