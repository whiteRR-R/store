from domain.entities.category import Category
from domain.value_objects.category_name import CategoryName
from application.dtos.category_dto import CategoryDTO


class CategoryFactory:
    @staticmethod
    def create_from_dto(category_dto: CategoryDTO):
        return Category(
            category_name=CategoryName(category_dto.name)
        )
