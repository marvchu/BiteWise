from fastapi import APIRouter, Query
from pydantic import BaseModel

from schemas.menu_items import MenuItemWithMetrics
from services import menu_items as menu_items_service

router = APIRouter(tags=["homepage"])

SECTION_LIMIT = 5  # items shown per homepage section, kept small for a fast first load


class HomepageResponse(BaseModel):
    best_protein_per_dollar: list[MenuItemWithMetrics]
    best_calories_per_dollar: list[MenuItemWithMetrics]
    meals_under_price: list[MenuItemWithMetrics]
    # active_deals intentionally omitted until the deals endpoint/model exists


@router.get("/homepage", response_model=HomepageResponse)
def get_homepage(under_price: float = Query(default=10.0, ge=0)):
    """
    Assembles the homepage sections from the user flow doc.

    This just composes calls to the menu-items service — no new
    business logic lives here. If this grows more complex (e.g.
    once deals/personalization are added), move it into a
    services/homepage.py module.
    """
    return HomepageResponse(
        best_protein_per_dollar=menu_items_service.get_menu_items(sort="protein_per_dollar")[:SECTION_LIMIT],
        best_calories_per_dollar=menu_items_service.get_menu_items(sort="calories_per_dollar")[:SECTION_LIMIT],
        meals_under_price=menu_items_service.get_menu_items(max_price=under_price, sort="price")[:SECTION_LIMIT],
    )