from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.domain.models import FullOrderItem, Round


class OrderResponse(BaseModel):
    created: datetime
    paid: bool
    subtotal: float
    taxes: float
    discounts: float
    items: List[FullOrderItem]
    rounds: List[Round]


class AddRoundResponse(BaseModel):
    message: str
    order: OrderResponse


class PayOrderResponse(BaseModel):
    message: str
    order: OrderResponse
