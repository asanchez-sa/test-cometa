from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItem(BaseModel):
    name: str
    quantity: int


class FullOrderItem(OrderItem):
    price_per_unit: float = 0
    total: float = 0


class Round(BaseModel):
    created: datetime
    items: List[OrderItem]


class Order(BaseModel):
    created: datetime
    paid: bool = False
    subtotal: float = 0
    taxes: float = 0
    discounts: float = 0
    items: List[FullOrderItem] = []
    rounds: List[Round] = []


class AddRoundRequest(BaseModel):
    items: List[OrderItem]