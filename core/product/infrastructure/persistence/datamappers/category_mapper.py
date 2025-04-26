from domain.entities.category import Category
from infrastructure.persistence.models.category_model import CategoryModel


class CategoryDataMapper:
    def entity_to_model(self, category: Category) -> CategoryModel:
        """
        Converts a model object to an entity object.
        """
        return CategoryModel(
            id=category.id,
            name=category.name,
        )

    def model_to_entity(self, category_model: CategoryModel) -> Category:
        """
        Converts an entity object to a model object.
        """
        return Category(
            id=category_model.id,
            name=category_model.name,
        )
