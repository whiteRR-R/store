import re
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from domain.enums.role import Role


class UserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Field(Role.USER)

    @field_validator('password', mode='before')
    @classmethod
    def password_must_contain_letter_and_digit(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Пароль должен быть не менее 8 символов')
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'[A-Za-z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну букву')
        return value


class UserGatewayDTO(BaseModel):
    user_id: UUID
    username: str
    email: str
    hashed_password: bytes
    role: str
    status: str = "active"
