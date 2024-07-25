from fastapi import APIRouter, Depends, HTTPException
from app.application.services.order_service import OrderService
from app.api.dependencies import get_order_service
from app.domain.dto.response import ResponseDTO
from app.domain.models.order import AddRoundRequest

router = APIRouter()


@router.get("/order")
async def get_current_order(order_service: OrderService = Depends(get_order_service)):
    response = order_service.get_current_order()
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    return response.data


@router.post("/order/add-round")
async def add_round(request: AddRoundRequest, order_service: OrderService = Depends(get_order_service)):
    response = order_service.add_round(request.items)
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    return response.data
