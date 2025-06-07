from domain.entities.category import Category
from domain.value_objects.category_name import CategoryName
from application.dtos.category_dto import CreateCategoryDTO, CategoryDTO
from typing import Optional
from uuid import UUID


class CategoryFactory:
    
    @staticmethod
    def from_params(category_name: str, category_id: Optional[UUID] = None) -> Category:
        return Category(
            id=category_id,
            category_name=CategoryName(category_name),
        )
    
    @staticmethod
    def from_dto(category_dto: CreateCategoryDTO) -> Category:
        return Category(
            category_name=CategoryName(category_dto.name)
        )

    @staticmethod
    def to_dto(category: Category) -> CategoryDTO:
        return CategoryDTO(
            id=category.id,
            name=category.name.value
        )
