from dataclasses import dataclass
from uuid import UUID
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductAttribute:
    attribute_id: UUID
    value: str

    def __post_init__(self):
        if not isinstance(self.attribute_id, UUID):
            raise InvalidValueException("Value is not UUID type")
        if not self.value:
            raise InvalidValueException("Attribute value cannot be empty.")
        if len(self.value) < 3:
            raise InvalidValueException("Attribute value must be at least 3 characters long.")
        if len(self.value) > 50:
            raise InvalidValueException("Attribute value must be at most 50 characters long.")
        if not self.value.isalnum():
            raise InvalidValueException("Attribute value must be alphanumeric.")
        if not self.value[0].isalpha():
            raise InvalidValueException("Attribute value must start with a letter.")
        if not self.value:
            raise InvalidValueException("Attribute value cannot be empty.")

