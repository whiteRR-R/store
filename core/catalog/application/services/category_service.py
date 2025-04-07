from domain.entities.category import Category
from domain.interfaces.repository import CategoryRepositoryProtocol
from application.events.integration_events.category_create_event import CategoryCreateEvent
from application.interfaces.event_bus import EventBusPublisherProtocol


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepositoryProtocol,
        event_bus: EventBusPublisherProtocol,
    ) -> None:
        self.category_repository = category_repository
        self.event_bus = event_bus
    
    async def add_category(self, name: str, description: str):
        """Add a new category."""
        try:
            category = Category(name=name, description=description)
            event = CategoryCreateEvent(category_id=category.category_id, name=name)
            await self.event_bus.publish(event)
            await self.category_repository.add(category)
        except Exception as e:
            raise Exception(f"Failed to add category: {e}") from e
        
    async def get_all_categories(self) -> list[Category]:
        """Retrieve all categories."""
        return await self.category_repository.get_all()
