from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.menu_items import MenuItemWithMetrics
from services import menu_items as menu_items_service
from routers.location_params import user_coordinates

router = APIRouter(prefix="/menu-items", tags=["menu-items"])


@router.get("", response_model=list[MenuItemWithMetrics])
def list_menu_items(
    max_price: float | None = Query(default=None, ge=0),
    min_calories: float | None = Query(default=None, ge=0),
    max_calories: float | None = Query(default=None, ge=0),
    sort: str | None = Query(default=None),
    coordinates: tuple[float, float] | None = Depends(user_coordinates),
    db: Session = Depends(get_db),
):
    try:
        return menu_items_service.list_menu_items(
            db,
            max_price=max_price,
            min_calories=min_calories,
            max_calories=max_calories,
            sort=sort,
            coordinates=coordinates,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{menu_item_id}", response_model=MenuItemWithMetrics)
def read_menu_item(
    menu_item_id: int,
    coordinates: tuple[float, float] | None = Depends(user_coordinates),
    db: Session = Depends(get_db),
):
    item = menu_items_service.get_menu_item(db, menu_item_id, coordinates)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item
