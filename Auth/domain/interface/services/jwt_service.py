from abc import ABC, abstractmethod
from datetime import timedelta
from config import config_manager

class JWTServiceInterface(ABC):
    @abstractmethod
    async def _create_token(self, payload: dict, token_type: str, expire_time: timedelta) -> str:
        raise NotImplementedError
    
    @abstractmethod
    async def _decode_token(self, jwt_token: str):
        raise NotImplementedError
    
    @abstractmethod
    async def create_access_token(
        self,
        payload: dict,
        token_type: str = "access",
        expire_time_in_minutes: int = 15,
    ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    async def create_refresh_token(
        self,
        payload: dict,
        token_type: str = "refresh",
        expire_time_in_days: int = 20,
    ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    async def generate_jwt_tokens(self, subject: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_token_subject(self, jwt_token: str):
        raise NotImplementedError