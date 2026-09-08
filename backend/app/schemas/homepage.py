from typing import Optional

from pydantic import BaseModel, Field

from schemas.deals import DealSummary
from schemas.free_food_events import FreeFoodEventSummary
from schemas.menu_items import MenuItemWithMetrics


class HomepageResponse(BaseModel):
    """Price-first homepage contract.

    Nutrition rankings are enrichment for meals with restaurant-provided
    nutrition; they are not required for a meal to appear elsewhere.
    Empty deal and free-food collections make their current absence explicit
    without inventing records.
    """

    featured: Optional[MenuItemWithMetrics] = None
    meals_under_budget: list[MenuItemWithMetrics]
    active_deals: list[DealSummary] = Field(default_factory=list)
    free_food_today: list[FreeFoodEventSummary] = Field(default_factory=list)
    best_calories_per_dollar: list[MenuItemWithMetrics] = Field(default_factory=list)
