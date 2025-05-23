from domain.interfaces.repositories.category_repository import CategoryRepositoryProtocol
from application.events.integration.category_create_event import CategoryCreateEvent
from application.factories.category_factory import CategoryFactory
from uuid import UUID


class CategoryCreateHandler:
    def __init__(self, category_repository: CategoryRepositoryProtocol):
        self.category_repository = category_repository

    async def handle(self, event: CategoryCreateEvent):
        category = CategoryFactory.from_params(
            category_id=UUID(event.category_id),
            category_name=event.category_name
        )
        await self.category_repository.create(category)
