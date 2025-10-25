from typing import Protocol


class OutboxRepository(Protocol):
    async def add(self, event_type: str, payload: dict) -> None:
        ...
