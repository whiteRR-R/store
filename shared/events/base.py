from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BaseEvent:
    event_name: str
    timestamp: str

    def __init__(self, event_name: str):
        self.event_name = event_name
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)
