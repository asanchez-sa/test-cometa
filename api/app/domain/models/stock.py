from pydantic import BaseModel
from datetime import datetime
from typing import List
from .beer import Beer


class Stock(BaseModel):
    last_updated: datetime
    beers: List[Beer]