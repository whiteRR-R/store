from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    user_id: UUID
    username: str
    email: str
    role: str
    status: str

class UserCreateDTO(BaseModel):
    username: str
    email: str
    hashed_password: str
    role: str
    status: str

class UserEmailUpdateDTO(BaseModel):
    email: EmailStr
