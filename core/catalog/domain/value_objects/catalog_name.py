from dataclasses import dataclass
from domain.exceptions import (
    EmptyException,
    TooLongException,
    InvalidTypeException,
)

@dataclass(frozen=True)
class CategoryName:
    """Value object representing a category name."""
    value: str
    
    def __post_init__(self):
        if not self.value.strip():
            raise EmptyException("Catalog name cannot be empty or whitespace only")
        if len(self.value) > 100:
            raise TooLongException("Catalog name cannot exceed 100 characters")
        if self.value.isdigit():
            raise InvalidTypeException("Catalog name must be a string")
