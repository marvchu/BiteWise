from typing import Optional
from pydantic import BaseModel


class MenuItem(BaseModel):
    """Raw menu item data, as it would come from the database."""
    id: int
    restaurant_id: int
    name: str
    price: float
    protein_grams: Optional[float] = None
    calories: Optional[float] = None


class MenuItemWithMetrics(MenuItem):
    """Menu item enriched with computed value metrics.

    protein_per_dollar / calories_per_dollar are None when the
    underlying nutrition data isn't available, since those fields
    are optional per the architecture doc.
    """
    protein_per_dollar: Optional[float] = None
    calories_per_dollar: Optional[float] = None
