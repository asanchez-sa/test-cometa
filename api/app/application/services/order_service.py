from datetime import datetime
from typing import List
from app.domain.models import Order, Round, FullOrderItem, OrderItem
from app.application.interfaces.repositories.order_repository import OrderRepository
from app.application.services.stock_service import StockService
from app.domain.dto.response import ResponseDTO


class OrderService:
    def __init__(self, order_repository: OrderRepository, stock_service: StockService):
        self._order_repository = order_repository
        self._stock_service = stock_service

    def get_current_order(self) -> ResponseDTO:
        try:
            order = self._order_repository.get_current_order()
            if order is None:
                order = Order(created=datetime.now(), rounds=[], items=[])
                self._order_repository.update_order(order)
            return ResponseDTO.ok(order)
        except Exception as e:
            return ResponseDTO.fail(f"Error al obtener la orden actual: {str(e)}")

    def add_round(self, items: List[OrderItem]) -> ResponseDTO:
        if not items:
            return ResponseDTO.fail("La lista de items no puede estar vacía")

        try:
            order_response = self.get_current_order()
            if not order_response.success:
                return order_response

            order = order_response.data
            if order.paid:
                order = self._order_repository.create_new_order()

            stock_verification = self._verify_and_update_stock(items)
            if not stock_verification.success:
                return stock_verification

            new_round = Round(created=datetime.now(), items=items)
            order.rounds.append(new_round)

            update_result = self._update_order_items_and_subtotal(order, items)
            if not update_result.success:
                return update_result

            self._order_repository.update_order(order)

            return ResponseDTO.ok(order)
        except Exception as e:
            return ResponseDTO.fail(f"Error al añadir ronda: {str(e)}")

    def _verify_and_update_stock(self, items: List[OrderItem]) -> ResponseDTO:
        try:
            for item in items:
                beer = self._stock_service.get_beer(item.name)
                if beer.quantity < item.quantity:
                    return ResponseDTO.fail(f"No hay suficiente {item.name} en stock")
                self._stock_service.update_beer_quantity(item.name, beer.quantity - item.quantity)
            return ResponseDTO.ok(None)
        except Exception as e:
            return ResponseDTO.fail(f"Error al verificar o actualizar el stock: {str(e)}")

    def _update_order_items_and_subtotal(self, order: Order, items: List[OrderItem]) -> ResponseDTO:
        try:
            for item in items:
                beer = self._stock_service.get_beer(item.name)
                full_item = FullOrderItem(
                    name=item.name,
                    quantity=item.quantity,
                    price_per_unit=beer.price,
                    total=beer.price * item.quantity
                )
                order.items.append(full_item)
                order.subtotal += full_item.total
            return ResponseDTO.ok(None)
        except Exception as e:
            return ResponseDTO.fail(f"Error al actualizar los items de la orden: {str(e)}")