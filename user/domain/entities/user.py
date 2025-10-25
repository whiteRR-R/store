from uuid import UUID
from domain.enums.role import UserRole
from domain.enums.status import UserStatus


class User:
    def __init__(
        self,
        user_id: UUID,
        username: str,
        email: str,
        role: UserRole = UserRole.USER,
        status: UserStatus = UserStatus.INACTIVE,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
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
