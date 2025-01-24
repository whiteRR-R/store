from abc import ABC, abstractmethod
from datetime import  timedelta


class JWTSecurityInterface(ABC):
    @abstractmethod
    def encode_jwt(self, payload: dict, expire_timedelta: timedelta | None) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def decode_jwt(self, jwt_token: str):
        raise NotImplementedError
    