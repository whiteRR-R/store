from domain.aggregates.product import ProductRoot
from domain.value_objects.product_name import ProductName
from domain.value_objects.product_description import ProductDescription
from domain.value_objects.product_price import ProductPrice
from domain.value_objects.product_attribute import ProductAttribute
from domain.entities.category import Category
from domain.entities.brand import Brand
from application.dtos.product_dto import ProductDTO
from application.dtos.product_dto import AttributeDTO
from typing import List


class ProductFactory:
    @staticmethod
    def from_dto(
        dto: ProductDTO,
        brand: Brand,
        categories: List[Category]
    ) -> ProductRoot:
        
        attributes = [
            ProductAttribute(attr.key, attr.value) for attr in dto.attributes
        ]
        
        return ProductRoot(
            name=ProductName(dto.name),
            brand=brand,
            description=ProductDescription(dto.description),
            price=ProductPrice(dto.price),
            categories=categories,
            attributes=attributes,
        )

    @staticmethod
    def to_dto(product: ProductRoot) -> ProductDTO:
        return ProductDTO(
            id=product.id,
            name=product.name.value,
            brand_id=product.brand.id,
            description=product.description.value,
            price=product.price.value,
            category_ids=[category.id for category in product.categories],
            attributes=[
                AttributeDTO(key=key, value=value)
                for key, value in product.attributes.items()
            ],
        )
