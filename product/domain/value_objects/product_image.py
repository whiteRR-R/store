from dataclasses import dataclass
from domain.exceptions import InvalidValueException


@dataclass(frozen=True)
class ProductImage:
    url: str
    
    def __post_init__(self):
        if not self.url:
            raise InvalidValueException("Product image URL cannot be empty.")
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            raise InvalidValueException("Product image URL must start with 'http://' or 'https://'.")
        if len(self.url) < 10:
            raise InvalidValueException("Product image URL must be at least 10 characters long.")
        if len(self.url) > 200:
            raise InvalidValueException("Product image URL must be at most 200 characters long.")
