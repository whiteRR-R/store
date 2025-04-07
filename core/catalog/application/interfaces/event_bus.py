from typing import Protocol


class EventBusPublisherProtocol(Protocol):
    def publish(self, event: str) -> None:
        """Publish an event to the event bus."""
        pass
