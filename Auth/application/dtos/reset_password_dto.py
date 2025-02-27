from dataclasses import dataclass


@dataclass(frozen=True)
class ResetPasswordDTO:
    reset_token: str
    new_password: bytes
