from typing import Optional

from sqlalchemy.orm import Session

from models.restaurant import Restaurant as RestaurantModel
from schemas.restaurants import RestaurantDetail, RestaurantSearchResult
from services.menu_items import list_menu_items


def restaurant_address(restaurant: RestaurantModel) -> str | None:
    return restaurant.locations[0].address if restaurant.locations else None


def search_restaurants(
    db: Session,
    query: Optional[str] = None,
    max_price: Optional[float] = None,
) -> list[RestaurantSearchResult]:
    """Return restaurants with menu items matching the food query and budget."""
    normalized_query = query.strip().casefold() if query else None
    eligible_items = list_menu_items(db, max_price=max_price, sort="price")
    results: list[RestaurantSearchResult] = []

    for restaurant in db.query(RestaurantModel).all():
        matching_items = [
            item
            for item in eligible_items
            if item.restaurant_id == restaurant.id
            and (
                normalized_query is None
                or normalized_query in item.name.casefold()
                or (item.category is not None and normalized_query in item.category.casefold())
            )
        ]
        if not matching_items:
            continue

        results.append(
            RestaurantSearchResult(
                id=restaurant.id,
                name=restaurant.name,
                address=restaurant_address(restaurant),
                matching_items=matching_items,
                lowest_matching_price=matching_items[0].price,
            )
        )

    return sorted(results, key=lambda result: result.lowest_matching_price)


def get_restaurant(db: Session, restaurant_id: int) -> Optional[RestaurantDetail]:
    restaurant = db.get(RestaurantModel, restaurant_id)
    if restaurant is None:
        return None

    menu_items = [
        item for item in list_menu_items(db, sort="price")
        if item.restaurant_id == restaurant_id
    ]
    return RestaurantDetail(
        id=restaurant.id,
        name=restaurant.name,
        address=restaurant_address(restaurant),
        menu_items=menu_items,
    )
