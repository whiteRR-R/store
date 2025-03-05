from typing import Protocol
from datetime import timedelta
from config import config_manager


class JWTServiceProtocol(Protocol):
    async def _create_token(self, payload: dict, token_type: str, expire_time: timedelta) -> str:
        ...

    async def _decode_token(self, jwt_token: str):
        ...

    async def create_reset_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.RESET_TOKEN_TYPE,
        expire_time_in_minutes: int = config_manager.jwt.reset_token_expire_time_minute,
    ) -> str:
        ...

    async def create_access_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.ACCESS_TOKEN_TYPE,
        expire_time_in_minutes: int = config_manager.jwt.access_token_expire_time_minute,
    ) -> str:
        ...

    async def create_refresh_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.REFRESH_TOKEN_TYPE,
        expire_time_in_days: int = config_manager.jwt.refresh_token_expire_time_day,
    ) -> str:
        ...

    async def generate_jwt_tokens(self, subject: str):
        ...

    async def validate_token_type(self, jwt_token: str, token_type: str):
        ...

    async def get_token_subject(self, jwt_token: str):
        ...
