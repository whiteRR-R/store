from domain.exceptions import ValidationError
from dataclasses import dataclass


@dataclass(frozen=True)
class Username:
    """Value Object для Username с проверкой длины и содержания"""
    value: str

    def __post_init__(self):
        self._validate_username()

    def __repr__(self):
        return self.value
    
    def _validate_username(self):
        """Проверка, что username соответствует правилам"""
        if not self.value:
            raise ValidationError("Username cannot be an empty string.")
        if ' ' in self.value:
            raise ValidationError("Username cannot contain spaces.")
        if len(self.value) < 3 or len(self.value) > 20:
            raise ValidationError(f"Username '{self.value}' must be between 3 and 20 characters.")
        if not self.value.isalnum():
            raise ValidationError(f"Username '{self.value}' can only contain alphanumeric characters.")

