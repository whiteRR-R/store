from decimal import Decimal
from domain.entities.order import OrderStatus


def test_initial_order_state(order):
    assert order.status == OrderStatus.PENDING
    assert order.total == Decimal("0.00")
    assert order.get_items() == []
    assert order.created_at is not None
    assert order.updated_at is None
    assert order.shipped_at is None
    assert order.cancelled_at is None

def test_pay_transitions_status_and_sets_updated_at(order):
    order.pay()
    assert order.status == OrderStatus.PAID
    assert order.updated_at is not None

def test_pay_does_not_work_if_not_pending(order):
    order.status = OrderStatus.SHIPPED
    order.pay()
    assert order.status is not OrderStatus.PAID
    assert order.status == OrderStatus.SHIPPED

def test_add_order_item(order, order_item):
    order.add_item(order_item)
    order_items = order.get_items()
    assert order_item in order_items
    assert order.total == order_item.price * order_item.quantity
    
def test_add_order_item_not_allowed_when_not_pending(order, order_item):
    order.status = OrderStatus.PAID
    order.add_item(order_item)
    order_items = order.get_items()
    assert order_item not in order_items

def test_remove_item_updates_total(order, order_item):
    order.add_item(order_item)
    order.remove_item(order_item)
    assert len(order.get_items()) == 0
    assert order.total == Decimal("0.00")
    assert order.updated_at is not None

def test_remove_item_nonexisting_item_does_nothing(order, order_item):
    order.remove_item(order_item)
    assert len(order.get_items()) == 0
    assert order.total == Decimal("0.00")

def test_ship_works_only_after_paid(order):
    order.pay()
    order.ship()
    assert order.status == OrderStatus.SHIPPED
    assert order.shipped_at is not None
    assert order.updated_at is not None

def test_confirm_works_only_after_ship(order):
    order.pay()
    order.ship()
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED
    assert order.updated_at is not None

def test_cancel_works_only_when_status_paid(order):
    order.pay()
    order.cancel()
    assert order.status == OrderStatus.CANCELLED
    assert order.updated_at is not None
