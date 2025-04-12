from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class CategoryName:
    name: str
    
    def __post_init__(self):
        if not self.name:
            raise InvalidValueException("Brand name cannot be empty.")
        if len(self.name) < 3:
            raise InvalidValueException("Brand name must be at least 3 characters long.")
        if len(self.name) > 50:
            raise InvalidValueException("Brand name must be at most 50 characters long.")
        if not self.name.isalnum():
            raise InvalidValueException("Brand name must be alphanumeric.")
        if not self.name[0].isalpha():
            raise InvalidValueException("Brand name must start with a letter.")
