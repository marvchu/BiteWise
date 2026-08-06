from typing import Optional

from pydantic import BaseModel

from schemas.menu_items import MenuItemWithMetrics


class Restaurant(BaseModel):
    id: int
    name: str
    address: Optional[str] = None


class RestaurantSearchResult(Restaurant):
    matching_items: list[MenuItemWithMetrics]
    lowest_matching_price: float


class RestaurantDetail(Restaurant):
    menu_items: list[MenuItemWithMetrics]
