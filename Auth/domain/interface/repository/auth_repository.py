from typing import Protocol
from domain.entities.user import User


class AuthRepositoryProtocol(Protocol):
    async def find_by_username(self, username: str):
        ...

    async def find_by_email(self, email: str):
        ...

    async def update(self, user: User):
        ...
