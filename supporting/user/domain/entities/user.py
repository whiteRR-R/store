from uuid import UUID
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

    def __repr__(self):
        return self.value

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    
    def __repr__(self):
        return self.value


class User:
    def __init__(
        self,
        user_id: UUID,
        username: str,
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.USER,
        status: UserStatus = UserStatus.INACTIVE,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.status = status

    def change_role(self, new_role: UserRole, actor_role: UserRole):
        if actor_role != UserRole.ADMIN:
            raise PermissionError("Only admin can change roles")
        self.role = new_role
    
    def change_email(self, new_email: str):
        if not new_email:
            raise ValueError("Invalid email")
        self.email = new_email

    def activate(self):
        self.status = UserStatus.ACTIVE

    def deactivate(self):
        self.status = UserStatus.INACTIVE
    
    def ban(self):
        self.status = UserStatus.BANNED
