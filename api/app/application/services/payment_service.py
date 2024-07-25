from app.domain.models import Order
from app.application.interfaces.repositories.order_repository import OrderRepository


class PaymentService:
    def __init__(self, order_repository: OrderRepository):
        self._order_repository = order_repository

    def pay_order(self) -> Order:
        order = self._order_repository.get_current_order()
        if order.paid:
            raise ValueError("La orden ya ha sido pagada")

        order.taxes = order.subtotal * 0.19

        try:
            self._order_repository.update_order(order)

            order.paid = True
            self._order_repository.update_order(order)

            new_order = self._order_repository.create_new_order()
            self._order_repository.update_order(new_order)
        except Exception as e:
            raise Exception(f"Error al procesar el pago: {str(e)}")

        return order
