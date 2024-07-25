from fastapi import APIRouter, Depends
from app.application.services.stock_service import StockService
from app.api.dependencies import get_stock_service
from app.domain.models import Stock

router = APIRouter()


@router.get("/stock", response_model=Stock)
async def get_stock(stock_service: StockService = Depends(get_stock_service)):
    return stock_service.get_stock()