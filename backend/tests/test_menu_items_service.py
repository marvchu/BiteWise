import pytest

from app.schemas.menu_items import MenuItem
from app.services import menu_items


def test_compute_metrics_calculates_value_metrics():
    item = MenuItem(
        id=100,
        restaurant_id=10,
        name="Test Bowl",
        price=8.00,
        protein_grams=24,
        calories=640,
    )

    result = menu_items.compute_metrics(item)

    assert result.protein_per_dollar == 3.0
    assert result.calories_per_dollar == 80.0


def test_compute_metrics_uses_none_when_price_is_zero():
    item = MenuItem(
        id=101,
        restaurant_id=10,
        name="Promo Meal",
        price=0,
        protein_grams=20,
        calories=500,
    )

    result = menu_items.compute_metrics(item)

    assert result.protein_per_dollar is None
    assert result.calories_per_dollar is None


def test_list_menu_items_filters_by_max_price_and_min_protein():
    result = menu_items.list_menu_items(max_price=8.00, min_protein=30)

    assert [item.name for item in result] == ["Double Cheeseburger", "Grilled Chicken Sandwich"]


def test_list_menu_items_sorts_by_price_ascending():
    result = menu_items.list_menu_items(sort="price")

    assert [item.price for item in result] == sorted(item.price for item in result)


def test_list_menu_items_sorts_by_protein_per_dollar_descending_with_missing_last():
    result = menu_items.list_menu_items(sort="protein_per_dollar")

    metric_values = [item.protein_per_dollar for item in result]
    present_values = [value for value in metric_values if value is not None]

    assert present_values == sorted(present_values, reverse=True)
    assert metric_values[-1] is None


def test_list_menu_items_rejects_invalid_sort_key():
    with pytest.raises(ValueError):
        menu_items.list_menu_items(sort="distance")


def test_get_menu_item_returns_metrics_for_existing_item():
    result = menu_items.get_menu_item(1)

    assert result is not None
    assert result.name == "Chicken Burrito Bowl"
    assert result.protein_per_dollar == 4.74


def test_get_menu_item_returns_none_for_missing_item():
    assert menu_items.get_menu_item(999) is None
