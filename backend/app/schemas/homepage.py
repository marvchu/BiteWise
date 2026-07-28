from pydantic import BaseModel

from schemas.menu_items import MenuItemWithMetrics


class HomepageResponse(BaseModel):
    best_protein_per_dollar: list[MenuItemWithMetrics]
    best_calories_per_dollar: list[MenuItemWithMetrics]
    meals_under_price: list[MenuItemWithMetrics]
    # active_deals intentionally omitted until the deals endpoint/model exists
