from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FreeFoodEventSummary(BaseModel):
    id: int
    title: str
    host_name: str
    location_name: str
    starts_at: datetime
    ends_at: Optional[datetime] = None
