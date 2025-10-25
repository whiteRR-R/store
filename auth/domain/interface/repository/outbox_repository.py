from typing import Protocol


class OutboxRepository(Protocol):
    async def add(self, event: Event) -> None:
        ...
