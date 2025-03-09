from pydantic import BaseModel


class ResetPasswordDTO(BaseModel):
    reset_token: str
    new_password: str
