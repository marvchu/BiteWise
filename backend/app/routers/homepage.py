from fastapi import APIRouter, Query

from schemas.homepage import HomepageResponse
from services import menu_items as menu_items_service

router = APIRouter(tags=["homepage"])

SECTION_LIMIT = 5  # items shown per homepage section, kept small for a fast first load


@router.get("/homepage", response_model=HomepageResponse)
def get_homepage(max_price: float = Query(default=10.0, ge=0)):
    """
    Assembles the homepage sections from the user flow doc.

    This just composes calls to the menu-items service — no new
    business logic lives here. If this grows more complex (e.g.
    once deals/personalization are added), move it into a
    services/homepage.py module.
    """
    meals_under_budget = menu_items_service.list_menu_items(
        max_price=max_price, sort="price"
    )[:SECTION_LIMIT]

    return HomepageResponse(
        featured=meals_under_budget[0] if meals_under_budget else None,
        meals_under_budget=meals_under_budget,
        active_deals=[],
        free_food_today=[],
        best_protein_per_dollar=menu_items_service.list_menu_items(
            min_protein=0, sort="protein_per_dollar"
        )[:SECTION_LIMIT],
        best_calories_per_dollar=menu_items_service.list_menu_items(
            min_calories=0, sort="calories_per_dollar"
        )[:SECTION_LIMIT],
    )
