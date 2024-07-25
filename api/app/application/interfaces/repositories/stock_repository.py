from abc import ABC, abstractmethod
from app.domain.models import Stock, Beer


class StockRepository(ABC):
    @abstractmethod
    def get_stock(self) -> Stock:
        pass

    @abstractmethod
    def update_stock(self, stock: Stock) -> None:
        pass

    @abstractmethod
    def get_beer(self, name: str) -> Beer:
        pass

    @abstractmethod
    def update_beer(self, beer: Beer) -> None:
        pass
