from domain.entities.brand import Brand
from application.factories.brand_factory import BrandFactory
from infrastructure.persistence.models.brand_model import BrandModel


class BrandDataMapper:
    def entity_to_model(self, brand: Brand) -> BrandModel:
        """
        Converts a model object to an entity object.
        """
        return BrandModel(
            id=brand._id,
            name=brand.name,
        )
    
    def model_to_entity(self, brand_model: BrandModel) -> Brand:
        """
        Converts an entity object to a model object.
        """
        return BrandFactory.from_params(
            brand_id=brand_model.id,
            brand_name=brand_model.name,
        )

