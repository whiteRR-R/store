from exceptions import InvalidRoleException
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    """Value Object для Role с проверкой длины и содержания"""
    role: str

    def __post_init__(self):
        self._validate_role()
    
    def __repr__(self):
        return self.role

    def _validate_role(self):
        """Проверка, что role соответствует правилам"""
        if not self.role:
            raise InvalidRoleException("Role cannot be an empty string.")
        if ' ' in self.role:
            raise InvalidRoleException("Role cannot contain spaces.")
        if len(self.role) <= 3:
            raise InvalidRoleException(f"Role '{self.role}' must be more than 3 characters")
        if not self.role.isalnum():
            raise InvalidRoleException(f"Role '{self.role}' can only contain alphanumeric characters.")    
    