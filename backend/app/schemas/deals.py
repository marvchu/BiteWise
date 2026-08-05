from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DealType(str, Enum):
    STUDENT_DISCOUNT = "student_discount"
    BOGO = "bogo"
    HAPPY_HOUR = "happy_hour"
    FIXED_PRICE = "fixed_price"
    PERCENT_OFF = "percent_off"
    FREE_ITEM = "free_item"


class DealSummary(BaseModel):
    id: int
    restaurant_id: int
    menu_item_id: Optional[int] = None
    title: str
    deal_type: DealType
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
