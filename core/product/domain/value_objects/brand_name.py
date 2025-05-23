from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class BrandName:
    """
    A value object representing a brand name.

    Attributes:
        name (str): The name of the brand.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValueException("Brand name cannot be empty.")
        if len(self.value) < 3:
            raise InvalidValueException("Brand name must be at least 3 characters long.")
        if len(self.value) > 50:
            raise InvalidValueException("Brand name must be at most 50 characters long.")
        if not self.value.isalnum():
            raise InvalidValueException("Brand name must be alphanumeric.")
        if not self.value[0].isalpha():
            raise InvalidValueException("Brand name must start with a letter.")
