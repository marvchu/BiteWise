from fastapi import APIRouter, HTTPException, Query

from schemas.restaurants import RestaurantDetail, RestaurantSearchResult
from services import restaurants as restaurants_service

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[RestaurantSearchResult])
def list_restaurants(
    query: str | None = Query(default=None, min_length=1),
    max_price: float | None = Query(default=None, ge=0),
):
    return restaurants_service.search_restaurants(query=query, max_price=max_price)


@router.get("/{restaurant_id}", response_model=RestaurantDetail)
def read_restaurant(restaurant_id: int):
    restaurant = restaurants_service.get_restaurant(restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
