from fastapi import APIRouter, HTTPException, Query

from schemas.menu_items import MenuItemWithMetrics
from services import menu_items as menu_items_service

router = APIRouter(prefix="/menu-items", tags=["menu-items"])


@router.get("", response_model=list[MenuItemWithMetrics])
def list_menu_items(
    max_price: float | None = Query(default=None, ge=0),
    min_protein: float | None = Query(default=None, ge=0),
    sort: str | None = Query(default=None),
):
    try:
        return menu_items_service.get_menu_items(
            max_price=max_price, min_protein=min_protein, sort=sort
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{menu_item_id}", response_model=MenuItemWithMetrics)
def get_menu_item(menu_item_id: int):
    item = menu_items_service.get_menu_item(menu_item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item