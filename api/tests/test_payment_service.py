import pytest
from unittest.mock import Mock, call
from datetime import datetime
from app.application.services.payment_service import PaymentService
from app.domain.models import Order, FullOrderItem


@pytest.fixture
def mock_order_repository():
    return Mock()


@pytest.fixture
def payment_service(mock_order_repository):
    return PaymentService(mock_order_repository)


def test_pay_order_success(payment_service, mock_order_repository):
    current_order = Order(
        created=datetime.now(),
        paid=False,
        subtotal=100,
        taxes=0,
        items=[FullOrderItem(name="Test Beer", quantity=5, price_per_unit=20, total=100)]
    )
    new_order = Order(created=datetime.now(), paid=False, subtotal=0, taxes=0, items=[])

    mock_order_repository.get_current_order.return_value = current_order
    mock_order_repository.create_new_order.return_value = new_order

    result = payment_service.pay_order()

    assert result.paid == True
    assert result.taxes == pytest.approx(19)
    assert mock_order_repository.update_order.call_count == 3
    mock_order_repository.create_new_order.assert_called_once()

    expected_calls = [
        call(current_order),
        call(current_order),
        call(new_order)
    ]
    mock_order_repository.update_order.assert_has_calls(expected_calls, any_order=False)


def test_pay_already_paid_order(payment_service, mock_order_repository):
    paid_order = Order(
        created=datetime.now(),
        paid=True,
        subtotal=100,
        taxes=19,
        items=[FullOrderItem(name="Test Beer", quantity=5, price_per_unit=20, total=100)]
    )
    mock_order_repository.get_current_order.return_value = paid_order

    with pytest.raises(ValueError, match="La orden ya ha sido pagada"):
        payment_service.pay_order()

    mock_order_repository.update_order.assert_not_called()
    mock_order_repository.create_new_order.assert_not_called()


def test_pay_order_with_no_items(payment_service, mock_order_repository):
    empty_order = Order(created=datetime.now(), paid=False, subtotal=0, taxes=0, items=[])
    new_order = Order(created=datetime.now(), paid=False, subtotal=0, taxes=0, items=[])

    mock_order_repository.get_current_order.return_value = empty_order
    mock_order_repository.create_new_order.return_value = new_order

    result = payment_service.pay_order()

    assert result.paid == True
    assert result.taxes == 0
    assert mock_order_repository.update_order.call_count == 3
    mock_order_repository.create_new_order.assert_called_once()

    expected_calls = [
        call(empty_order),
        call(empty_order),
        call(new_order)
    ]
    mock_order_repository.update_order.assert_has_calls(expected_calls, any_order=False)


def test_pay_order_repository_error(payment_service, mock_order_repository):
    current_order = Order(
        created=datetime.now(),
        paid=False,
        subtotal=100,
        taxes=0,
        items=[FullOrderItem(name="Test Beer", quantity=5, price_per_unit=20, total=100)]
    )
    mock_order_repository.get_current_order.return_value = current_order
    mock_order_repository.update_order.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Error al procesar el pago: Database error"):
        payment_service.pay_order()

    assert current_order.paid == False
    mock_order_repository.update_order.assert_called_once_with(current_order)
    mock_order_repository.create_new_order.assert_not_called()
