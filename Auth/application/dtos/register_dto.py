from pydantic import BaseModel
from domain.valueobject.username import Username
from domain.valueobject.role import Role
from domain.valueobject.email import Email


class UserRegisterRequest(BaseModel):
    username: Username
    role: Role
    email: Email
    password: str