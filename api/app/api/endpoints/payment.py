from fastapi import APIRouter, Depends
from app.application.services.payment_service import PaymentService
from app.api.dependencies import get_payment_service
from app.domain.models import Order

router = APIRouter()


@router.post("/payment/order", response_model=Order)
async def pay_order(payment_service: PaymentService = Depends(get_payment_service)):
    return payment_service.pay_order()