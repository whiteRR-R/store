from dataclasses import dataclass
from domain.exceptions import (
    EmptyException,
    TooLongException,
    InvalidTypeException,
)


@dataclass(frozen=True)
class Description:
    """Value object representing a category description."""
    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise EmptyException("Description cannot be empty or whitespace only")
        if len(self.value) > 500:
            raise TooLongException("Description cannot exceed 500 characters")
        if self.value.isdigit():
            raise InvalidTypeException("Description must be a string")
