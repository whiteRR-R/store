from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductAttribute:
    key: str
    value: str

    def __post_init__(self):
        if not self.key:
            raise InvalidValueException("Attribute name cannot be empty.")
        if len(self.key) < 3:
            raise InvalidValueException("Attribute name must be at least 3 characters long.")
        if len(self.key) > 50:
            raise InvalidValueException("Attribute name must be at most 50 characters long.")
        if not self.key.isalnum():
            raise InvalidValueException("Attribute name must be alphanumeric.")
        if not self.key[0].isalpha():
            raise InvalidValueException("Attribute name must start with a letter.")
        if not self.value:
            raise InvalidValueException("Attribute value cannot be empty.")

