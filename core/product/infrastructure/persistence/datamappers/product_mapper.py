from domain.aggregates.product import ProductRoot
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.models.brand_model import BrandModel
from infrastructure.persistence.models.category_model import CategoryModel
from typing import Iterable

class ProductDataMapper:
    
    def entity_to_model(
        self,
        product: ProductRoot,
        brand: BrandModel,
        categories: Iterable[CategoryModel]
        
        ) -> ProductModel:
        """
        Converts a model object to an entity object.
        """
        return ProductModel(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            attributes=product.attributes,
            brand=brand,
            categories=categories
        )
    
    def model_to_entity(self):
        ...
    
    