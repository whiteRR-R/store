from domain.entities.category import Category
from domain.value_objects.catalog_name import CategoryName
from domain.value_objects.description import Description
from infrastructure.persistence.models.category import CategoryModel


class CategoryDataMapper:
    def model_to_entity(self, category_model: CategoryModel) -> Category:
        """Convert a CategoryModel to a Category entity."""
        return Category(
            id=category_model.id,
            name=CategoryName(category_model.name),
            description=Description(category_model.description),
        )
    
    def entity_to_model(self, category: Category) -> CategoryModel:
        """Convert a Category entity to a CategoryModel."""
        return CategoryModel(
            id=category.category_id,
            name=category.name,
            description=category.description,
        )
