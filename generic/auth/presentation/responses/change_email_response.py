from pydantic import BaseModel


class ChangeEmailResponse(BaseModel):
    message: str
