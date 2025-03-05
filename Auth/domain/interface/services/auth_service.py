from typing import Protocol


class AuthServiceProtocol(Protocol):
    async def create_user(self, user_dto) -> None:
        ...

    async def _existing_username_or_email(self, username: str, email: str) -> str:
        ...

    async def verify_user_credentials(self, user_credentials) -> None:
        ...

    async def get_user_by_username(self, username: str) -> None:
        ...

    async def get_user_by_email(self, email: str) -> None:
        ...
