"""
Core menu-item business logic: value-metric calculation, filtering,
and sorting. Kept separate from routers so it can be reused by both
the /menu-items endpoint and the /homepage endpoint (and, later, a
mobile client hitting the same API).
"""
from typing import Optional

from db.stub_data import get_all_menu_items
from schemas.menu_items import MenuItem, MenuItemWithMetrics

VALID_SORT_KEYS = {"protein_per_dollar", "calories_per_dollar", "price"}


def compute_metrics(item: MenuItem) -> MenuItemWithMetrics:
    """Attach protein-per-dollar / calories-per-dollar to a menu item.

    Metrics are None if the source nutrition data is missing, or if
    price is 0 (avoids a division error on free/promo items).
    """
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
    max_price: Optional[float] = None,
    min_protein: Optional[float] = None,
    min_calories: Optional[float] = None,
    max_calories: Optional[float] = None,
    sort: Optional[str] = None,
) -> list[MenuItemWithMetrics]:
    """Fetch, filter, and sort menu items.

    This is the single source of truth for "what counts as a good
    value item" — the homepage service calls this instead of
    re-implementing filtering/sorting.
    """
    items = [compute_metrics(item) for item in get_all_menu_items()]

    if max_price is not None:
        items = [i for i in items if i.price <= max_price]

    if min_protein is not None:
        items = [
            i for i in items
            if i.protein_grams is not None and i.protein_grams >= min_protein
        ]

    if min_calories is not None:
        items = [i for i in items if i.calories is not None and i.calories >= min_calories]

    if max_calories is not None:
        items = [i for i in items if i.calories is not None and i.calories <= max_calories]

    if sort is not None:
        if sort not in VALID_SORT_KEYS:
            raise ValueError(f"Invalid sort key: {sort}. Must be one of {VALID_SORT_KEYS}")

        ascending = sort == "price"  # cheaper is better; higher value-per-dollar is better
        missing_last = lambda i: getattr(i, sort) is None  # noqa: E731

        if ascending:
            items.sort(key=lambda i: (missing_last(i), getattr(i, sort) or 0))
        else:
            items.sort(key=lambda i: (missing_last(i), -(getattr(i, sort) or 0)))

    return items


def get_menu_item(menu_item_id: int) -> Optional[MenuItemWithMetrics]:
    from db.stub_data import get_menu_item_by_id
    item = get_menu_item_by_id(menu_item_id)
    return compute_metrics(item) if item else None
