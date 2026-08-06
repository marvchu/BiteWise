from typing import Optional

from db.stub_data import get_all_restaurants, get_restaurant_by_id
from schemas.restaurants import RestaurantDetail, RestaurantSearchResult
from services.menu_items import list_menu_items


def search_restaurants(
    query: Optional[str] = None,
    max_price: Optional[float] = None,
) -> list[RestaurantSearchResult]:
    """Return restaurants with menu items matching the food query and budget."""
    normalized_query = query.strip().casefold() if query else None
    eligible_items = list_menu_items(max_price=max_price, sort="price")
    results: list[RestaurantSearchResult] = []

    for restaurant in get_all_restaurants():
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
                **restaurant.model_dump(),
                matching_items=matching_items,
                lowest_matching_price=matching_items[0].price,
            )
        )

    return sorted(results, key=lambda result: result.lowest_matching_price)


def get_restaurant(restaurant_id: int) -> Optional[RestaurantDetail]:
    restaurant = get_restaurant_by_id(restaurant_id)
    if restaurant is None:
        return None

    menu_items = [
        item for item in list_menu_items(sort="price")
        if item.restaurant_id == restaurant_id
    ]
    return RestaurantDetail(**restaurant.model_dump(), menu_items=menu_items)
