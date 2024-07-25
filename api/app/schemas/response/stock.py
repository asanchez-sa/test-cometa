from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.domain.models import Beer


class StockResponse(BaseModel):
    last_updated: datetime
    beers: List[Beer]