from typing import Protocol
from domain.entities.user import User


class AuthRepositoryProtocol(Protocol):
    """ Интерфейс репозитория для работы с пользователями. """
    async def find_by_username(self, username: str):
        """ Находит пользователя по его имени (username). """
        ...

    async def find_by_email(self, email: str):
        """ Находит пользователя по его почте (email). """
        ...
