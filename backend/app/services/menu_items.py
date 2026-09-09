"""
Core menu-item business logic: value-metric calculation, filtering,
and sorting.
"""
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from models.menu_item import MenuItem as MenuItemModel
from models.restaurant import Restaurant
from schemas.menu_items import MenuItem, MenuItemWithMetrics
from services.distance import nearest_location
from schemas.locations import LocationSummary

VALID_SORT_KEYS = {"calories_per_dollar", "price", "distance_miles"}


def model_to_schema(item: MenuItemModel, coordinates=None) -> MenuItem:
    location, distance = nearest_location(item.restaurant.locations, coordinates)
    return MenuItem(
        id=item.id,
        restaurant_id=item.restaurant_id,
        restaurant_name=item.restaurant.name,
        name=item.name,
        price=float(item.price),
        price_max=float(item.price_max) if item.price_max is not None else None,
        category=item.category,
        calories=item.calories,
        calories_max=item.calories_max,
        distance_miles=distance,
        location=LocationSummary(
            id=location.id, address=location.address,
            latitude=float(location.latitude), longitude=float(location.longitude),
        ) if location else None,
    )


def compute_metrics(item: MenuItem) -> MenuItemWithMetrics:
    """Attach calories-per-dollar to a menu item."""
    calories_per_dollar = None

    if item.price > 0:
        if item.calories is not None:
            calories_per_dollar = round(item.calories / item.price, 2)

    return MenuItemWithMetrics(
        **item.model_dump(),
        calories_per_dollar=calories_per_dollar,
    )


def list_menu_items(
    db: Session,
    max_price: Optional[float] = None,
    min_calories: Optional[float] = None,
    max_calories: Optional[float] = None,
    sort: Optional[str] = None,
    coordinates: tuple[float, float] | None = None,
) -> list[MenuItemWithMetrics]:
    """Fetch menu items from the database, then enrich and sort them."""
    query = db.query(MenuItemModel).options(
        joinedload(MenuItemModel.restaurant).selectinload(Restaurant.locations)
    )

    if max_price is not None:
        query = query.filter(MenuItemModel.price <= max_price)

    if min_calories is not None:
        query = query.filter(MenuItemModel.calories.is_not(None))
        query = query.filter(MenuItemModel.calories >= min_calories)

    if max_calories is not None:
        query = query.filter(MenuItemModel.calories.is_not(None))
        query = query.filter(MenuItemModel.calories <= max_calories)

    items = [compute_metrics(model_to_schema(item, coordinates)) for item in query.all()]

    if sort is not None:
        if sort not in VALID_SORT_KEYS:
            raise ValueError(f"Invalid sort key: {sort}. Must be one of {VALID_SORT_KEYS}")

        if sort == "distance_miles" and coordinates is None:
            raise ValueError("Location is required to sort by distance")
        ascending = sort in {"price", "distance_miles"}
        missing_last = lambda i: getattr(i, sort) is None  # noqa: E731

        if ascending:
            items.sort(key=lambda i: (missing_last(i), getattr(i, sort) or 0, i.price, i.id))
        else:
            items.sort(key=lambda i: (missing_last(i), -(getattr(i, sort) or 0)))

    return items


def get_menu_item(db: Session, menu_item_id: int, coordinates=None) -> Optional[MenuItemWithMetrics]:
    item = (
        db.query(MenuItemModel)
        .options(joinedload(MenuItemModel.restaurant))
        .filter(MenuItemModel.id == menu_item_id)
        .one_or_none()
    )
    return compute_metrics(model_to_schema(item, coordinates)) if item else None
