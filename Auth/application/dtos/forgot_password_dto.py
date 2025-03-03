from pydantic import BaseModel


class ForgotPasswordDTO(BaseModel):
    email: str
