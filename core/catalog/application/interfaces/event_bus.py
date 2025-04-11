from typing import Protocol, Any
from application.interfaces.event import EventProtocol


class EventBusPublisherProtocol(Protocol):
    async def publish(self, event: EventProtocol) -> None:
        """Publish an event to the event bus."""
        pass
