from pydantic import BaseModel, Field, EmailStr, field_validator
from domain.exceptions import ValidationError
import re


class UserDTO(BaseModel):
    username: str
    email: EmailStr
    password: bytes
    role: str = 'user'

    @field_validator('password', mode='before')
    @classmethod
    def password_must_contain_letter_and_digit(cls, value: str) -> bytes:
        if len(value) < 8:
            raise ValidationError('Пароль должен быть не менее 8 символов')
        if not re.search(r'\d', value):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Пароль должен содержать хотя бы одну букву')
        return value.encode('utf-8')
