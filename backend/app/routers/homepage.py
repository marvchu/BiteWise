from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.homepage import HomepageResponse
from services import menu_items as menu_items_service

router = APIRouter(tags=["homepage"])

SECTION_LIMIT = 5


@router.get("/homepage", response_model=HomepageResponse)
def get_homepage(max_price: float = Query(default=10.0, ge=0), db: Session = Depends(get_db)):
    meals_under_budget = menu_items_service.list_menu_items(
        db, max_price=max_price, sort="price"
    )[:SECTION_LIMIT]

    return HomepageResponse(
        featured=meals_under_budget[0] if meals_under_budget else None,
        meals_under_budget=meals_under_budget,
        active_deals=[],
        free_food_today=[],
        best_protein_per_dollar=menu_items_service.list_menu_items(
            db, min_protein=0, sort="protein_per_dollar"
        )[:SECTION_LIMIT],
        best_calories_per_dollar=menu_items_service.list_menu_items(
            db, min_calories=0, sort="calories_per_dollar"
        )[:SECTION_LIMIT],
    )
