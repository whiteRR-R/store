from domain.entities.category import Category
from infrastructure.persistence.datamapper.category_mapper import CategoryDataMapper
from infrastructure.persistence.models.category import CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper  = CategoryDataMapper()

    async def add(self, category: Category):
        """Add a new category to the repository."""
        category_model = self._mapper.entity_to_model(category)
        self._session.add(category_model)
        await self._session.commit()
    
    async def get_all(self) -> list[dict]:
        """Retrieve all categories from the repository."""
        categories = await self._session.execute(
            select(CategoryModel)
        )
        categories_as_dict = [
            self._mapper.model_to_dict(category_model)
            for category_model in categories.scalars().all()
        ]
        return categories_as_dict
        

