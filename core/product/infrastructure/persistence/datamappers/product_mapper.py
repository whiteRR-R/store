from typing import Iterable
from domain.aggregates.product import ProductRoot
from domain.value_objects.product_attribute import ProductAttribute
from domain.value_objects.product_description import ProductDescription
from domain.value_objects.product_image import ProductImage
from domain.value_objects.product_name import ProductName
from domain.value_objects.product_price import ProductPrice
from application.factories.brand_factory import BrandFactory
from application.factories.category_factory import CategoryFactory
from infrastructure.persistence.models.product_model import ProductModel
from infrastructure.persistence.models.image_model import ProductImageModel


class ProductDataMapper:
    
    def entity_to_model(
        self,
        product: ProductRoot,
        ) -> ProductModel:
        """
        Converts a entity object to an model object.
        """
        
        product_model = ProductModel(
            id=product.id,
            name=product.name.value,
            description=product.description.value,
            price=product.price.value,
            attributes=product.attributes,
        )
        
        product_model.images = [
            ProductImageModel(url=url)
            for url in product_model.images
        ]
        
        return product_model
    
    def model_to_entity(self, product_model: ProductModel) -> ProductRoot:
        """
        Converts a model object to an entity object.
        """
        attributes = [
            ProductAttribute(attr_id, attr_value) for attr_id, attr_value in product_model.attributes.items()
        ]
        categories = [
            CategoryFactory.from_params(category_id=category.id, category_name=category.name)
            for category in product_model.categories
        ]
        brand = BrandFactory.from_params(
            brand_id=product_model.brand.id,
            brand_name=product_model.brand.name
        )
        
        images = [ProductImage(image.url) for image in product_model.images]
        
        return ProductRoot(
            id=product_model.id,
            name=ProductName(product_model.name),
            brand=brand,
            description=ProductDescription(product_model.description),
            price=ProductPrice(product_model.price),
            categories=categories,
            attributes=attributes,
            images=images
        )
        
    
    