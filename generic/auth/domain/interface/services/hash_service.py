from typing import Protocol


class PasswordHasherProtocol(Protocol):
    def hash(self, password: str) -> bytes:
        """Хеширует пароль."""
        ...

    def verify(self, password: str, stored_hash: bytes) -> bool:
        """Проверяет пароль на соответствие хешу."""
        ...
