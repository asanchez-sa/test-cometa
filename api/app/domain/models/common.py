from pydantic import BaseModel


class OrderItem(BaseModel):
    name: str
    quantity: int