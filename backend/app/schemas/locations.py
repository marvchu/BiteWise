from pydantic import BaseModel


class LocationSummary(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
