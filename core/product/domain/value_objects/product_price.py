from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductPrice:
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidValueException("Product price must be a positive integer.")
