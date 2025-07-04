from typing import Protocol
from domain.entities.user import User


class AuthRepositoryProtocol(Protocol):
    
    async def add(self, user: User):
        """ Добавляет пользователя в репозиторий. """
        ...
        
    async def update(self, user: User):
        """ Обновляет данные пользователя в репозитории. """
        ...
    
    async def delete(self, user: User):
        """ Удаляет пользователя из репозитория. """
        ...
    
    """ Интерфейс репозитория для работы с пользователями. """
    async def get_by_username(self, username: str) -> User:
        """ Отдает пользователя по его имени (username). """
        ...

    async def get_by_email(self, email: str) -> User:
        """ Отдает пользователя по его почте (email). """
        ...
