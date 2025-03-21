from domain.exceptions import InvalidUsernameException
from dataclasses import dataclass


@dataclass(frozen=True)
class Username:
    """Value Object для Username с проверкой длины и содержания"""
    username: str

    def __post_init__(self):
        self._validate_username()

    def __repr__(self):
        return self.username
    
    def _validate_username(self):
        """Проверка, что username соответствует правилам"""
        if not self.username:
            raise InvalidUsernameException("Username cannot be an empty string.")
        if ' ' in self.username:
            raise InvalidUsernameException("Username cannot contain spaces.")
        if len(self.username) < 3 or len(self.username) > 20:
            raise InvalidUsernameException(f"Username '{self.username}' must be between 3 and 20 characters.")
        if not self.username.isalnum():
            raise InvalidUsernameException(f"Username '{self.username}' can only contain alphanumeric characters.")

