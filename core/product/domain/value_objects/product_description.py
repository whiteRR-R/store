from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductDescription:
    description: str

    def __post_init__(self):
        if not self.description:
            raise InvalidValueException("Product description cannot be empty.")
        if len(self.description) < 10:
            raise InvalidValueException("Product description must be at least 10 characters long.")
        if len(self.description) > 500:
            raise InvalidValueException("Product description must be at most 500 characters long.")
        if not self.description[0].isalpha():
            raise InvalidValueException("Product description must start with a letter.")
