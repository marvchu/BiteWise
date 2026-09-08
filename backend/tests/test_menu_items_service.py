import pytest

from app.schemas.menu_items import MenuItem
from app.services import menu_items


def test_compute_metrics_calculates_calorie_value_metric():
    item = MenuItem(
        id=100,
        restaurant_id=10,
        name="Test Bowl",
        price=8.00,
        calories=640,
    )

    result = menu_items.compute_metrics(item)

    assert result.calories_per_dollar == 80.0


def test_compute_metrics_uses_none_when_price_is_zero():
    item = MenuItem(
        id=101,
        restaurant_id=10,
        name="Promo Meal",
        price=0,
        calories=500,
    )

    result = menu_items.compute_metrics(item)

    assert result.calories_per_dollar is None


def test_list_menu_items_filters_by_max_price(db):
    result = menu_items.list_menu_items(db, max_price=8.00)

    assert [item.name for item in result] == ["Double Cheeseburger", "Grilled Chicken Sandwich", "Veggie Burrito"]


def test_list_menu_items_sorts_by_price_ascending(db):
    result = menu_items.list_menu_items(db, sort="price")

    assert [item.price for item in result] == sorted(item.price for item in result)


def test_list_menu_items_rejects_invalid_sort_key(db):
    with pytest.raises(ValueError):
        menu_items.list_menu_items(db, sort="distance")


def test_get_menu_item_returns_metrics_for_existing_item(db):
    result = menu_items.get_menu_item(db, 1)

    assert result is not None
    assert result.name == "Chicken Burrito Bowl"


def test_get_menu_item_returns_none_for_missing_item(db):
    assert menu_items.get_menu_item(db, 999) is None
