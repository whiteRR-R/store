from typing import Protocol
from datetime import timedelta
from application.dtos.jwt_token_dto import JWTTokensDTO
from config import config_manager


class JWTServiceProtocol(Protocol):
    def _create_token(
        self,
        payload: dict,
        token_type: str,
        expire_time: timedelta,
    ) -> str:
        """Генерует токен для пользователя"""
        ...

    def decode_token(self, jwt_token: str):
        """Декодитует токен"""
        ...

    def create_access_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.ACCESS_TOKEN_TYPE,
        expire_time_in_minutes: int = config_manager.jwt.access_token_expire_time_minute,
    ) -> str:
        """Генерует access токен для пользователя"""
        ...

    def create_refresh_token(
        self,
        payload: dict,
        token_type: str = config_manager.jwt.REFRESH_TOKEN_TYPE,
        expire_time_in_days: int = config_manager.jwt.refresh_token_expire_time_day,
    ) -> str: ...

    def generate_jwt_tokens(self, subject: str) -> JWTTokensDTO:
        """Генерует refresh и access токены и возвращает их"""
        ...

    def validate_token_type(self, jwt_token: str, token_type: str):
        """Проверяет, соответствует ли тип токена ожидаемому, и возвращает subject токена."""
        ...

    def get_token_subject(self, jwt_token: str):
        """Возвращает subject токена"""
        ...
