from app.domain.models import Stock, Beer
from app.application.interfaces.repositories.stock_repository import StockRepository


class StockService:
    def __init__(self, stock_repository: StockRepository):
        self._stock_repository = stock_repository

    def get_stock(self) -> Stock:
        return self._stock_repository.get_stock()

    def get_beer(self, name: str) -> Beer:
        return self._stock_repository.get_beer(name)

    def update_beer_quantity(self, name: str, quantity: int) -> None:
        beer = self.get_beer(name)
        beer.quantity = quantity
        self._stock_repository.update_beer(beer)