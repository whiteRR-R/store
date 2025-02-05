from pydantic import BaseModel


class ForgotPasswordRequest(BaseModel):
    email: str

class ForgotPasswordResponse(BaseModel):
    email: str
    reset_token: str