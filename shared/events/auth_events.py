from dataclasses import dataclass
from events.base import BaseEvent

@dataclass
class UserRegisteredEvent(BaseEvent):
    user_id: str
    email: str
    username: str

    def __init__(self, user_id: str, email: str, username: str):
        super().__init__("user_registered")
        self.user_id = user_id
        self.email = email
        self.username = username


@dataclass
class UserCreationFailedEvent(BaseEvent):
    user_id: str
    reason: str

    def __init__(self, user_id: str, reason: str):
        super().__init__("user_creation_failed")
        self.user_id = user_id
        self.reason = reason
