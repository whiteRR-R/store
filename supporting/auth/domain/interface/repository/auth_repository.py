from typing import Protocol
from domain.entities.user import User


class AuthRepositoryProtocol(Protocol):
    """ Интерфейс репозитория для работы с пользователями. """
    async def get_by_username(self, username: str):
        """ Отдает пользователя по его имени (username). """
        ...

    async def get_by_email(self, email: str):
        """ Отдает пользователя по его почте (email). """
        ...
