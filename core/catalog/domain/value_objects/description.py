from dataclasses import dataclass
from exceptions import (
    EmptyException,
    TooLongException,
    InvalidTypeException,
)


@dataclass(frozen=True)
class Description:
    description: str

    def __post_init__(self):
        if not self.description.strip():
            raise EmptyException("Description cannot be empty or whitespace only")
        if len(self.description) > 500:
            raise TooLongException("Description cannot exceed 500 characters")
        if self.description.isdigit():
            raise InvalidTypeException("Description must be a string")
