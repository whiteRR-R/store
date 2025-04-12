from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductPrice:
    price: int

    def __post_init__(self):
        if self.price <= 0:
            raise InvalidValueException("Product price must be a positive integer.")
