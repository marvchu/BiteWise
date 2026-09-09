from typing import Optional
from pydantic import BaseModel
from schemas.locations import LocationSummary


class MenuItem(BaseModel):
    """Raw menu item data, as it would come from the database."""
    id: int
    restaurant_id: int
    restaurant_name: Optional[str] = None
    name: str
    price: float
    price_max: Optional[float] = None
    category: Optional[str] = None
    calories: Optional[float] = None
    calories_max: Optional[float] = None
    distance_miles: Optional[float] = None
    location: Optional[LocationSummary] = None


class MenuItemWithMetrics(MenuItem):
    """Menu item enriched with computed value metrics.

    calories_per_dollar is None when price or calorie data is unavailable.
    """
    calories_per_dollar: Optional[float] = None
