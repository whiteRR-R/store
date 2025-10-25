from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductName:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValueException("Product name cannot be empty.")
        if len(self.value) < 3:
            raise InvalidValueException("Product name must be at least 3 characters long.")
        if len(self.value) > 50:
            raise InvalidValueException("Product name must be at most 50 characters long.")
        if not self.value.isalnum():
            raise InvalidValueException("Product name must be alphanumeric.")
        if not self.value[0].isalpha():
            raise InvalidValueException("Product name must start with a letter.")
