"""
Temporary in-memory data standing in for real database queries.

Replace this module's contents with actual DB calls (e.g. SQLAlchemy
queries) once the database layer is designed. Everything downstream
(services, routers) should keep working unchanged as long as this
module keeps returning MenuItem objects.
"""
from schemas.menu_items import MenuItem
from schemas.restaurants import Restaurant

RESTAURANTS: list[Restaurant] = [
    Restaurant(id=1, name="Telegraph Taqueria", address="Telegraph Avenue, Berkeley"),
    Restaurant(id=2, name="Campus Cafe", address="Bancroft Way, Berkeley"),
    Restaurant(id=3, name="Bancroft Korean", address="Bancroft Way, Berkeley"),
]

MENU_ITEMS: list[MenuItem] = [
    MenuItem(id=1, restaurant_id=1, name="Chicken Burrito Bowl", price=9.50, category="bowl", calories=650),
    MenuItem(id=2, restaurant_id=1, name="Veggie Burrito", price=8.00, category="burrito", calories=550),
    MenuItem(id=3, restaurant_id=2, name="Double Cheeseburger", price=6.50, category="burger", calories=780),
    MenuItem(id=4, restaurant_id=2, name="Grilled Chicken Sandwich", price=7.25, category="sandwich", calories=520),
    MenuItem(id=5, restaurant_id=3, name="Bibimbap", price=11.00, category="rice", calories=600),
    MenuItem(id=6, restaurant_id=3, name="Ramen", price=10.50, category="noodles", calories=None),
]


def get_all_menu_items() -> list[MenuItem]:
    return MENU_ITEMS


def get_menu_item_by_id(menu_item_id: int) -> MenuItem | None:
    return next((item for item in MENU_ITEMS if item.id == menu_item_id), None)


def get_all_restaurants() -> list[Restaurant]:
    return RESTAURANTS


def get_restaurant_by_id(restaurant_id: int) -> Restaurant | None:
    return next((item for item in RESTAURANTS if item.id == restaurant_id), None)
