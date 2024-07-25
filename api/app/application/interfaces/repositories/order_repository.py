from abc import ABC, abstractmethod
from app.domain.models import Order


class OrderRepository(ABC):
    @abstractmethod
    def get_current_order(self) -> Order:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> None:
        pass

    @abstractmethod
    def create_new_order(self) -> Order:
        pass
