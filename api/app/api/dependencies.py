from fastapi import Depends
from app.application.services.stock_service import StockService
from app.application.services.order_service import OrderService
from app.application.services.payment_service import PaymentService
from app.infrastructure.repositories.in_memory_stock_repository import InMemoryStockRepository
from app.infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository

stock_repository = InMemoryStockRepository()
order_repository = InMemoryOrderRepository()


def get_stock_service():
    return StockService(stock_repository)


def get_order_service(stock_service: StockService = Depends(get_stock_service)):
    return OrderService(order_repository, stock_service)


def get_payment_service():
    return PaymentService(order_repository)
