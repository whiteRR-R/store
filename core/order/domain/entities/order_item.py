class OrderItem:
    def __init__(self, product_id: str, quantity: int, price: int):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"OrderItem(product_id={self.product_id}, quantity={self.quantity})"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }
