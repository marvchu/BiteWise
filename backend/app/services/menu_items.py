"""
Core menu-item business logic: value-metric calculation, filtering,
and sorting.
"""
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from models.menu_item import MenuItem as MenuItemModel
from schemas.menu_items import MenuItem, MenuItemWithMetrics

VALID_SORT_KEYS = {"protein_per_dollar", "calories_per_dollar", "price"}


def model_to_schema(item: MenuItemModel) -> MenuItem:
    return MenuItem(
        id=item.id,
        restaurant_id=item.restaurant_id,
        restaurant_name=item.restaurant.name,
        name=item.name,
        price=float(item.price),
        category=item.category,
        protein_grams=float(item.protein_grams) if item.protein_grams is not None else None,
        calories=item.calories,
    )


def compute_metrics(item: MenuItem) -> MenuItemWithMetrics:
    """Attach protein-per-dollar / calories-per-dollar to a menu item."""
    protein_per_dollar = None
    calories_per_dollar = None

    if item.price > 0:
        if item.protein_grams is not None:
            protein_per_dollar = round(item.protein_grams / item.price, 2)
        if item.calories is not None:
            calories_per_dollar = round(item.calories / item.price, 2)

    return MenuItemWithMetrics(
        **item.model_dump(),
        protein_per_dollar=protein_per_dollar,
        calories_per_dollar=calories_per_dollar,
    )


def list_menu_items(
    db: Session,
    max_price: Optional[float] = None,
    min_protein: Optional[float] = None,
    min_calories: Optional[float] = None,
    max_calories: Optional[float] = None,
    sort: Optional[str] = None,
) -> list[MenuItemWithMetrics]:
    """Fetch menu items from the database, then enrich and sort them."""
    query = db.query(MenuItemModel).options(joinedload(MenuItemModel.restaurant))

    if max_price is not None:
        query = query.filter(MenuItemModel.price <= max_price)

    if min_protein is not None:
        query = query.filter(MenuItemModel.protein_grams.is_not(None))
        query = query.filter(MenuItemModel.protein_grams >= min_protein)

    if min_calories is not None:
        query = query.filter(MenuItemModel.calories.is_not(None))
        query = query.filter(MenuItemModel.calories >= min_calories)

    if max_calories is not None:
        query = query.filter(MenuItemModel.calories.is_not(None))
        query = query.filter(MenuItemModel.calories <= max_calories)

    items = [compute_metrics(model_to_schema(item)) for item in query.all()]

    if sort is not None:
        if sort not in VALID_SORT_KEYS:
            raise ValueError(f"Invalid sort key: {sort}. Must be one of {VALID_SORT_KEYS}")

        ascending = sort == "price"
        missing_last = lambda i: getattr(i, sort) is None  # noqa: E731

        if ascending:
            items.sort(key=lambda i: (missing_last(i), getattr(i, sort) or 0))
        else:
            items.sort(key=lambda i: (missing_last(i), -(getattr(i, sort) or 0)))

    return items


def get_menu_item(db: Session, menu_item_id: int) -> Optional[MenuItemWithMetrics]:
    item = (
        db.query(MenuItemModel)
        .options(joinedload(MenuItemModel.restaurant))
        .filter(MenuItemModel.id == menu_item_id)
        .one_or_none()
    )
    return compute_metrics(model_to_schema(item)) if item else None
