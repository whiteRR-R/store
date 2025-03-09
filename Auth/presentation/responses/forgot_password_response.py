from pydantic import BaseModel


class ForgotPasswordResponse(BaseModel):
    email: str
    reset_token: str
