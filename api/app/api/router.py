from fastapi import APIRouter
from app.api.endpoints import stock, order, payment

router = APIRouter()

router.include_router(stock.router, tags=["stock"])
router.include_router(order.router, tags=["order"])
router.include_router(payment.router, tags=["payment"])
