from datetime import datetime
from app.domain.models import Order
from app.application.interfaces.repositories.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._current_order = None
        self._orders = []

    def get_current_order(self) -> Order:
        if self._current_order is None:
            self._current_order = Order(created=datetime.now(), rounds=[], items=[])
            self._orders.append(self._current_order)
        return self._current_order

    def update_order(self, order: Order) -> None:
        if self._current_order and self._current_order.created == order.created:
            self._current_order = order
        else:
            self._orders.append(order)
            self._current_order = order

    def create_new_order(self) -> Order:
        new_order = Order(created=datetime.now(), rounds=[], items=[])
        self._orders.append(new_order)
        self._current_order = new_order
        return new_order

    def get_all_orders(self) -> list[Order]:
        return self._orders
