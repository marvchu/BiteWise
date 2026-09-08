from db.base import Base
from models import Location, MenuItem, Restaurant


def test_initial_database_tables_are_registered():
    assert set(Base.metadata.tables) == {
        "restaurants",
        "locations",
        "menu_items",
    }


def test_restaurant_relationships_match_initial_schema():
    assert Restaurant.locations.property.mapper.class_ is Location
    assert Restaurant.menu_items.property.mapper.class_ is MenuItem
    assert Location.restaurant.property.mapper.class_ is Restaurant
    assert MenuItem.restaurant.property.mapper.class_ is Restaurant


def test_menu_item_nullable_nutrition_columns_match_product_rules():
    menu_items = Base.metadata.tables["menu_items"]

    assert menu_items.c.calories.nullable is True
    assert menu_items.c.price.nullable is False
