from domain.entities.category import Category
from domain.entities.brand import Brand
from domain.value_objects.product_name import ProductName
from domain.value_objects.product_image import ProductImage
from domain.value_objects.product_attribute import ProductAttribute
from domain.value_objects.product_image import ProductImage
from domain.value_objects.product_description import ProductDescription
from domain.value_objects.product_price import ProductPrice
from domain.exceptions import AlreadyExistException, NotFoundException, InvalidOperationException
from typing import List, Optional, Dict, MutableSequence
from uuid import uuid4, UUID


class ProductRoot:
    def __init__(
        self,
        name: ProductName,
        brand: Brand,
        description: ProductDescription,
        price: ProductPrice, 
        categories: MutableSequence[Category],
        attributes: MutableSequence[ProductAttribute],
        images: MutableSequence[ProductImage],
        id: Optional[UUID] = None,
    ) -> None:
        self._id = id or uuid4()
        self._name = name
        self._brand = brand
        self._description = description
        self._price = price
        self._categories = categories
        self._attributes = attributes
        self._images = images  
        
    def add_image(self, image: ProductImage) -> None:
        self._images.append(image)
    
    def remove_image(self, image: ProductImage) -> None:
        if len(self._images) <= 1:
            raise InvalidOperationException("Need to add image first")
        self._images.remove(image)

    def add_attribute(self, attribute: ProductAttribute) -> None:
        if attribute in self._attributes:
            raise AlreadyExistException(f"Attribute: {attribute} already exist")
        self._attributes.append(attribute)
    
    def remove_attribute(self, attribute: ProductAttribute) -> None:
        if len(self._attributes) <= 1:
            raise InvalidOperationException("Need to add attribute first")
        if attribute not in self._attributes:
            raise NotFoundException(f"Attribute: {attribute} does not exist")
        self._attributes.remove(attribute)
    
    def add_category(self, category: Category) -> None:
        if category in self._categories:
            raise AlreadyExistException(f"Category: {category} already exist")
        self._categories.append(category)
    
    def remove_category(self, category: Category) -> None:
        if len(self._categories) <= 1:
            raise InvalidOperationException("Need to add category first")
        if category not in self._categories:
            raise NotFoundException(f"Category: {category} does not exist")
        self._categories.remove(category)
    
    def update_description(self, description: ProductDescription) -> None:
        self._description = description
    
    def update_price(self, price: ProductPrice):
        self._price = price
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def name(self) -> ProductName:
        return self._name

    @property
    def brand(self) -> Brand:
        return self._brand
    
    @property
    def description(self) -> ProductDescription:
        return self._description
    
    @property
    def price(self) -> ProductPrice:
        return self._price
    
    @property
    def categories(self) -> List[Category]:
        return [category for category in self._categories]
    
    @property
    def attributes(self) -> Dict[str, str]:
        return {attribute.key: attribute.value for attribute in self._attributes}
    
    @property
    def images(self) -> List[str]:
        return [image.url for image in self._images]
    
    def __repr__(self) -> str:
        return (
            f"<Product: {self.name}, "
            f"Brand: {self.brand}, "
            f"Price: {self.price}, "
            f"Categories: {self.categories}"
        )
