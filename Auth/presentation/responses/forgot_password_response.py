from pydantic import BaseModel


class ForgotPasswordResponse(BaseModel):
    email: str
