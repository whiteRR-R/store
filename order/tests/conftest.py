import uuid
import pytest
from domain.value_objects.order_item import OrderItem
from domain.entities.order import Order


@pytest.fixture
def order_item():
    return OrderItem(
        product_id=uuid.uuid4(),
        quantity=3,
        price=20_000
    )


@pytest.fixture
def order():
    return Order(
        order_id=uuid.uuid4(),
        customer_id=uuid.uuid4()
    )
