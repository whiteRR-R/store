from domain.entities.category import Category
from domain.entities.brand import Brand
from domain.value_objects.product_name import ProductName
from domain.value_objects.product_image import ProductImage
from domain.value_objects.product_attribute import ProductAttribute
from domain.value_objects.product_description import ProductDescription
from domain.value_objects.product_price import ProductPrice
from domain.exceptions import AlreadyExistException
from typing import Optional, List, MutableSequence


class Product:
    def __init__(
        self,
        name: ProductName,
        brand: Brand,
        description: ProductDescription,
        price: ProductPrice, 
        categories: MutableSequence[Category],
        attributes: MutableSequence[ProductAttribute],
        images: MutableSequence[ProductImage],
    ) -> None:
        self._name = name
        self._brand = brand
        self._description = description
        self._price = price
        self._categories = categories
        self._attributes = attributes
        self._images = images  
        
    def add_image(self, image: ProductImage) -> None:
        self._images.append(image)
    
    def add_attribute(self, attribute: ProductAttribute) -> None:
        self._attributes.append(attribute)
    
    def add_category(self, category: Category) -> None:
        if category in self._categories:
            raise AlreadyExistException("Category already exist")
        self._categories.append(category)
    
    def update_description(self, description: ProductDescription) -> None:
        self._description = description
    
    def update_price(self, price: ProductPrice):
        self._price = price
    
    @property
    def name(self):
        return self._name.value

    @property
    def brand(self):
        return self._brand._name
    
    @property
    def description(self):
        return self._description.value
    
    @property
    def price(self):
        return self._price.value
    
    @property
    def categories(self) -> List[Category]:
        return [category for category in self._categories]
    
    @property
    def attributes(self) -> List[ProductAttribute]:
        return [attribute for attribute in self._attributes]
    
    @property
    def images(self) -> List[ProductImage]:
        return [image for image in self._images]
    
    def __repr__(self) -> str:
        return (
            f"<Product: {self.name}, "
            f"Brand: {self.brand}, "
            f"Price: {self.price}, "
            f"Categories: {[category.name for category in self.categories]}>"
        )
        
    
