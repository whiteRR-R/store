from domain.entities.category import Category
from domain.value_objects.category_name import CategoryName
from application.dtos.category_dto import CategoryDTO
from typing import Optional
from uuid import UUID


class CategoryFactory:
    
    @staticmethod
    def create(category_name: str, category_id: Optional[UUID] = None) -> Category:
        return Category(
            id=category_id,
            category_name=CategoryName(category_name),
        )
    
    @staticmethod
    def create_from_dto(category_dto: CategoryDTO) -> Category:
        return Category(
            category_name=CategoryName(category_dto.name)
        )
