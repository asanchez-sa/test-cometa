from datetime import datetime

from app.application.interfaces.repositories.stock_repository import StockRepository
from app.domain.models import Stock, Beer


class InMemoryStockRepository(StockRepository):
    def __init__(self):
        self._stock = Stock(
            last_updated=datetime.now(),
            beers=[
                Beer(name="Corona", price=115, quantity=200),
                Beer(name="Quilmes", price=120, quantity=200),
                Beer(name="Club Colombia", price=110, quantity=300)
            ]
        )

    def get_stock(self) -> Stock:
        return self._stock

    def update_stock(self, stock: Stock) -> None:
        self._stock = stock

    def get_beer(self, name: str) -> Beer:
        for beer in self._stock.beers:
            if beer.name == name:
                return beer
        raise ValueError(f"Beer with name {name} not found")

    def update_beer(self, updated_beer: Beer) -> None:
        for i, beer in enumerate(self._stock.beers):
            if beer.name == updated_beer.name:
                self._stock.beers[i] = updated_beer
                self._stock.last_updated = datetime.now()
                return
        raise ValueError(f"Beer with name {updated_beer.name} not found")