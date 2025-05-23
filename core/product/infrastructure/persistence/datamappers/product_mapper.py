from domain.aggregates.product import ProductRoot
from domain.value_objects.product_attribute import ProductAttribute
from domain.value_objects.product_description import ProductDescription
from domain.value_objects.product_name import ProductName
from domain.value_objects.product_price import ProductPrice
from application.factories.brand_factory import BrandFactory
from application.factories.category_factory import CategoryFactory
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
        Converts a entity object to an model object.
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
    
    def model_to_entity(self, product_model: ProductModel) -> ProductRoot:
        """
        Converts a model object to an entity object.
        """
        attributes = [
            ProductAttribute(key, value) for key, value in product_model.attributes.items()
        ]
        categories = [
            CategoryFactory.from_params(category_id=category.id, category_name=category.name)
            for category in product_model.categories
        ]
        brand = BrandFactory.from_params(
            brand_id=product_model.brand.id,
            brand_name=product_model.brand.name
        )
        
        return ProductRoot(
            id=product_model.id,
            name=ProductName(product_model.name),
            brand=brand,
            description=ProductDescription(product_model.description),
            price=ProductPrice(product_model.price),
            categories=categories,
            attributes=attributes,
        )
        
    
    