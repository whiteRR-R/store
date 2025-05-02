from typing import Protocol, Any


class UseCaseProtocol(Protocol):
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the use case with the provided arguments.
        """
        ...
