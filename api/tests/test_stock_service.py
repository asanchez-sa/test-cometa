import pytest
from unittest.mock import Mock
from datetime import datetime
from app.application.services.stock_service import StockService
from app.domain.models import Stock, Beer


@pytest.fixture
def mock_stock_repository():
    return Mock()


@pytest.fixture
def stock_service(mock_stock_repository):
    return StockService(mock_stock_repository)


def test_get_stock(stock_service, mock_stock_repository):
    current_time = datetime.now()
    expected_stock = Stock(
        last_updated=current_time,
        beers=[
            Beer(name="Corona", price=10, quantity=5),
            Beer(name="Club Colombia", price=12, quantity=3)
        ]
    )
    mock_stock_repository.get_stock.return_value = expected_stock

    result = stock_service.get_stock()

    assert result == expected_stock
    assert result.last_updated == current_time
    mock_stock_repository.get_stock.assert_called_once()


def test_get_beer(stock_service, mock_stock_repository):
    expected_beer = Beer(name="Corona", price=10, quantity=5)
    mock_stock_repository.get_beer.return_value = expected_beer

    result = stock_service.get_beer("Corona")

    assert result == expected_beer
    mock_stock_repository.get_beer.assert_called_once_with("Corona")


def test_get_beer_not_found(stock_service, mock_stock_repository):
    mock_stock_repository.get_beer.side_effect = ValueError("Beer not found")

    with pytest.raises(ValueError, match="Beer not found"):
        stock_service.get_beer("NonexistentBeer")


def test_update_beer_quantity(stock_service, mock_stock_repository):
    initial_beer = Beer(name="Corona", price=10, quantity=5)
    mock_stock_repository.get_beer.return_value = initial_beer

    stock_service.update_beer_quantity("Corona", 3)

    mock_stock_repository.get_beer.assert_called_once_with("Corona")
    mock_stock_repository.update_beer.assert_called_once()
    updated_beer = mock_stock_repository.update_beer.call_args[0][0]
    assert updated_beer.name == "Corona"
    assert updated_beer.quantity == 3
    assert updated_beer.price == 10


def test_update_beer_quantity_not_found(stock_service, mock_stock_repository):
    mock_stock_repository.get_beer.side_effect = ValueError("Beer not found")

    with pytest.raises(ValueError, match="Beer not found"):
        stock_service.update_beer_quantity("NonexistentBeer", 3)

    mock_stock_repository.update_beer.assert_not_called()