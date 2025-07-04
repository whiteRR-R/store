from pydantic import BaseModel, EmailStr, field_validator
import re


class UserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = 'user'

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
