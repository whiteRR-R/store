from dataclasses import dataclass


@dataclass(frozen=True)
class ForgotPasswordDTO:
    email: str
