from pydantic import BaseModel


class ForgotPasswordRequest:
    email: str

class ForgotPasswordResponse:
    email: str
    reset_token: str