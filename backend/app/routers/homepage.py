from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.homepage import HomepageResponse
from services import menu_items as menu_items_service
from routers.location_params import user_coordinates

router = APIRouter(tags=["homepage"])

SECTION_LIMIT = 5


@router.get("/homepage", response_model=HomepageResponse)
def get_homepage(
    max_price: float | None = Query(default=None, ge=0),
    sort: Literal["price", "distance_miles"] = "price",
    coordinates: tuple[float, float] | None = Depends(user_coordinates),
    db: Session = Depends(get_db),
):
    if sort == "distance_miles" and coordinates is None:
        raise HTTPException(status_code=422, detail="Location is required to sort by distance")
    meals_under_budget = menu_items_service.list_menu_items(
        db, max_price=max_price, sort=sort, coordinates=coordinates
    )[:SECTION_LIMIT]
    featured_candidates = meals_under_budget or menu_items_service.list_menu_items(
        db, sort="price", coordinates=coordinates
    )[:1]

    return HomepageResponse(
        featured=featured_candidates[0] if featured_candidates else None,
        meals_under_budget=meals_under_budget,
        active_deals=[],
        free_food_today=[],
        best_calories_per_dollar=menu_items_service.list_menu_items(
            db, min_calories=0, sort="calories_per_dollar", coordinates=coordinates
        )[:SECTION_LIMIT],
    )
