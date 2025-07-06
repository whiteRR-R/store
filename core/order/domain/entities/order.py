from typing import List
from enum import Enum
from decimal import Decimal
from datetime import datetime
from domain.entities.order_item import OrderItem


class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Order:
    def __init__(self,  order_id: str, customer_id: str):
        self._order_id = order_id
        self._customer_id = customer_id
        self.total: Decimal = Decimal("0.00")
        self._items: List[OrderItem] = []
        self.status: OrderStatus = OrderStatus.PENDING
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime | None = None
        self.shipped_at: datetime | None = None
        self.cancelled_at: datetime | None = None
        
    def pay(self):
        if self.status == OrderStatus.PENDING:
            self.status = OrderStatus.PAID
            self.updated_at = datetime.now()
    
    def ship(self):
        if self.status == OrderStatus.PAID:
            self.status = OrderStatus.SHIPPED
            self.shipped_at = datetime.now()
            self.updated_at = datetime.now()
            
    def confirm(self):
        if self.status == OrderStatus.SHIPPED:
            self.status = OrderStatus.CONFIRMED
            self.updated_at = datetime.now()
    
    def cancel(self):
        if self.status in [OrderStatus.PENDING, OrderStatus.PAID]:
            self.status = OrderStatus.CANCELLED
            self.cancelled_at = datetime.now()
            self.updated_at = datetime.now()

    def add_item(self, item: OrderItem):
        if self.status is OrderStatus.PENDING:
            self._items.append(item)
            self.total += item.quantity * item.price
    
    def remove_item(self, item: OrderItem):
        if item in self._items:
            self._items.remove(item)
            self.total -= item.quantity * item.price    
            self.updated_at = datetime.now()
    
    def discount(self, amount: Decimal):
        if self.status is OrderStatus.PENDING:
            self.total -= amount
            if self.total < Decimal("0.00"):
                self.total = Decimal("0.00")
            self.updated_at = datetime.now()
            
    def get_items(self) -> List[OrderItem]:
        return self._items
