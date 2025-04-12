from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductAttribute:
    name: str
    value: str

    def __post_init__(self):
        if not self.name:
            raise InvalidValueException("Attribute name cannot be empty.")
        if len(self.name) < 3:
            raise InvalidValueException("Attribute name must be at least 3 characters long.")
        if len(self.name) > 50:
            raise InvalidValueException("Attribute name must be at most 50 characters long.")
        if not self.name.isalnum():
            raise InvalidValueException("Attribute name must be alphanumeric.")
        if not self.name[0].isalpha():
            raise InvalidValueException("Attribute name must start with a letter.")
        if not self.value:
            raise InvalidValueException("Attribute value cannot be empty.")

