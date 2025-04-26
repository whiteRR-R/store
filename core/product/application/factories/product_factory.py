from domain.aggregates.product import ProductRoot
from domain.value_objects.product_name import ProductName
from domain.value_objects.product_description import ProductDescription
from domain.value_objects.product_price import ProductPrice
from domain.value_objects.product_attribute import ProductAttribute
from domain.entities.category import Category
from domain.entities.brand import Brand
from application.dtos.product_dto import CreateProductDTO
from typing import List

class ProductFactory:
    @staticmethod
    def create_from_dto(
        dto: CreateProductDTO,
        brand: Brand,
        categories: List[Category]
    ) -> ProductRoot:
        
        attributes = [
            ProductAttribute(attr.name, attr.value) for attr in dto.attributes
        ]
        
        return ProductRoot(
            name=ProductName(dto.name),
            brand=brand,
            description=ProductDescription(dto.description),
            price=ProductPrice(dto.price),
            categories=categories,
            attributes=attributes,
        )
