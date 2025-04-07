from typing import Protocol, Any


class EventProtocol(Protocol):
    """Interface for an event."""

    def to_dict(self) -> dict[str, Any]:
        """Convert the event to a dictionary."""
        pass
