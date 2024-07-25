from pydantic import BaseModel
from typing import List
from app.domain.models import FullOrderItem


class AddRoundRequest(BaseModel):
    items: List[FullOrderItem]
