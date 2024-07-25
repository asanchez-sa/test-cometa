import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from app.application.services.order_service import OrderService
from app.domain.models import Order, OrderItem, Beer, FullOrderItem


@pytest.fixture
def mock_order_repository():
    return Mock()


@pytest.fixture
def mock_stock_service():
    return Mock()


@pytest.fixture
def order_service(mock_order_repository, mock_stock_service):
    return OrderService(mock_order_repository, mock_stock_service)


def test_get_current_order_existing(order_service, mock_order_repository):
    existing_order = Order(created=datetime.now(), rounds=[], items=[])
    mock_order_repository.get_current_order.return_value = existing_order

    result = order_service.get_current_order()

    assert result == existing_order
    mock_order_repository.get_current_order.assert_called_once()
    mock_order_repository.update_order.assert_not_called()


def test_get_current_order_new(order_service, mock_order_repository):
    mock_order_repository.get_current_order.return_value = None

    result = order_service.get_current_order()

    assert isinstance(result, Order)
    assert len(result.rounds) == 0
    assert len(result.items) == 0
    mock_order_repository.get_current_order.assert_called_once()
    mock_order_repository.update_order.assert_called_once()


def test_add_round_to_unpaid_order(order_service, mock_order_repository, mock_stock_service):
    current_order = Order(created=datetime.now(), rounds=[], items=[], paid=False)
    mock_order_repository.get_current_order.return_value = current_order
    mock_stock_service.get_beer.return_value = Beer(name="Test Beer", price=10, quantity=5)
    items = [OrderItem(name="Test Beer", quantity=2)]

    result = order_service.add_round(items)

    assert len(result.rounds) == 1
    assert len(result.items) == 1
    assert result.subtotal == 20
    mock_stock_service.update_beer_quantity.assert_called_once_with("Test Beer", 3)
    mock_order_repository.update_order.assert_called_once()


def test_add_round_to_paid_order(order_service, mock_order_repository, mock_stock_service):
    paid_order = Order(created=datetime.now(), rounds=[], items=[], paid=True)
    new_order = Order(created=datetime.now(), rounds=[], items=[], paid=False)
    mock_order_repository.get_current_order.return_value = paid_order
    mock_order_repository.create_new_order.return_value = new_order
    mock_stock_service.get_beer.return_value = Beer(name="Test Beer", price=10, quantity=5)
    items = [OrderItem(name="Test Beer", quantity=2)]

    result = order_service.add_round(items)

    assert result == new_order
    assert len(result.rounds) == 1
    assert len(result.items) == 1
    assert result.subtotal == 20
    mock_order_repository.create_new_order.assert_called_once()
    mock_stock_service.update_beer_quantity.assert_called_once_with("Test Beer", 3)
    mock_order_repository.update_order.assert_called_once()


def test_add_round_insufficient_stock(order_service, mock_order_repository, mock_stock_service):
    current_order = Order(created=datetime.now(), rounds=[], items=[], paid=False)
    mock_order_repository.get_current_order.return_value = current_order
    mock_stock_service.get_beer.return_value = Beer(name="Test Beer", price=10, quantity=1)
    items = [OrderItem(name="Test Beer", quantity=2)]

    with pytest.raises(ValueError, match="No hay suficiente Test Beer en stock"):
        order_service.add_round(items)

    mock_stock_service.update_beer_quantity.assert_not_called()
    mock_order_repository.update_order.assert_not_called()
