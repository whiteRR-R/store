from pydantic import BaseModel, EmailStr


class ChangeEmailDTO(BaseModel):
    new_email: EmailStr
