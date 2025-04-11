from uuid import UUID
from typing import Any


class CategoryCreateEvent:
    """Event triggered when a new category is created."""

    def __init__(self, category_id: UUID, name: str) -> None:
        self.category_id = category_id.hex
        self.name = name
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "event_type": "CategoryCreateEvent",
            "category_id": self.category_id,
            "name": self.name,
        }

    def __repr__(self) -> str:
        return f"CategoryCreateEvent(category_id={self.category_id}, name={self.name})"
