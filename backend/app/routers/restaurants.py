from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.restaurants import RestaurantDetail, RestaurantSearchResult
from services import restaurants as restaurants_service
from routers.location_params import user_coordinates

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[RestaurantSearchResult])
def list_restaurants(
    query: str | None = Query(default=None, min_length=1),
    max_price: float | None = Query(default=None, ge=0),
    sort: Literal["price", "distance_miles"] = "price",
    coordinates: tuple[float, float] | None = Depends(user_coordinates),
    db: Session = Depends(get_db),
):
    if sort == "distance_miles" and coordinates is None:
        raise HTTPException(status_code=422, detail="Location is required to sort by distance")
    return restaurants_service.search_restaurants(
        db, query=query, max_price=max_price, coordinates=coordinates, sort=sort
    )


@router.get("/{restaurant_id}", response_model=RestaurantDetail)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = restaurants_service.get_restaurant(db, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
