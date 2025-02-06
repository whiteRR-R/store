from decimal import Decimal
from value_objects.category import Category

class Product:
    def __init__(
        self, 
        name: str, 
        description: str, 
        category: Category,
        price: Decimal,
        quantity: int, 
    ):
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.quantity = quantity
    
    async def is_in_stock(self, quantity: int):
        """ Проверять есть ли товар в наличии"""
        return self.quantity > quantity
    
    async def reduce_stock(self, quantity: int):
        """ Уменьшает количество на складе"""
        if await self.is_in_stock(quantity):
            self.quantity -= quantity
    
    async def restock(self, quantity: int):
        """ Добавляет товар на склад """
        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0.")
        self.quantity += quantity
    
    async def update_price(self, new_price: Decimal):
        """ Обновляет цену продукта. """
        if new_price < 0:
            raise ValueError("Цена не должно быть меньше нуля")
        self.price = new_price
    
        
        
    
        