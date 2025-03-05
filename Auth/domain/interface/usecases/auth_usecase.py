from typing import Protocol


class AuthUseCaseProtocol(Protocol):
    async def register(self, username: str, role: str, email: str, password: str) -> None:
        ...

    async def login(self, username: str, password: str) -> None:
        ...

    async def get_current_user_info(self, jwt_token: str) -> None:
        ...

    async def generate_access_token_from_refresh(self, jwt_token: str) -> None:
        ...

    async def forgot_password(self, email: str) -> None:
        ...

    async def reset_password(self, jwt_token: str, new_password: bytes) -> None:
        ...
