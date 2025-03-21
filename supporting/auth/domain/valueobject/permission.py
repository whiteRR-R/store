from exceptions import InvalidPermissionException
from dataclasses import dataclass


@dataclass(frozen=True)
class Permission:
    """Value Object для Role с проверкой длины и содержания"""
    permission: str
    description: str

    def __post_init__(self):
        self._validate_permission()

    def __repr__(self):
        return self.permission
    
    def _validate_permission(self):
        """Проверка, что role соответствует правилам"""
        if not self.role:
            raise InvalidPermissionException("Role cannot be an empty string.")
        if ' ' in self.role:
            raise InvalidPermissionException("Role cannot contain spaces.")
        if len(self.role) <= 3:
            raise InvalidPermissionException(f"Role '{self.role}' must be more than 3 characters")
        if not self.role.isalnum():
            raise InvalidPermissionException(f"Role '{self.role}' can only contain alphanumeric characters.")    
    