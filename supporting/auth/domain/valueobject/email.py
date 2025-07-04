from domain.exceptions import ValidationError
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """Value Object для Email с проверкой формата"""
    email: str

    def __post_init__(self):
        self._validate_email()

    def __repr__(self):
        return self.email
    
    def _validate_email(self):
        """Проверка, что email соответствует стандартному формату"""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, self.email):
            raise ValidationError(f"Invalid email format: {self.email}")

