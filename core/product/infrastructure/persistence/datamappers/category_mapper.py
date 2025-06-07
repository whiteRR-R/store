from domain.entities.category import Category
from application.factories.category_factory import CategoryFactory
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
        return CategoryFactory.from_params(
            category_id=category_model.id,
            category_name=category_model.name,
        )
