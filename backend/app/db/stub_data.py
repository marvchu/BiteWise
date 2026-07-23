"""
Temporary in-memory data standing in for real database queries.

Replace this module's contents with actual DB calls (e.g. SQLAlchemy
queries) once the database layer is designed. Everything downstream
(services, routers) should keep working unchanged as long as this
module keeps returning MenuItem objects.
"""
from schemas.menu_items import MenuItem

MENU_ITEMS: list[MenuItem] = [
    MenuItem(id=1, restaurant_id=1, name="Chicken Burrito Bowl", price=9.50, protein_grams=45, calories=650),
    MenuItem(id=2, restaurant_id=1, name="Veggie Burrito", price=8.00, protein_grams=15, calories=550),
    MenuItem(id=3, restaurant_id=2, name="Double Cheeseburger", price=6.50, protein_grams=35, calories=780),
    MenuItem(id=4, restaurant_id=2, name="Grilled Chicken Sandwich", price=7.25, protein_grams=38, calories=520),
    MenuItem(id=5, restaurant_id=3, name="Bibimbap", price=11.00, protein_grams=28, calories=600),
    MenuItem(id=6, restaurant_id=3, name="Ramen", price=10.50, protein_grams=None, calories=None),
]


def get_all_menu_items() -> list[MenuItem]:
    return MENU_ITEMS


def get_menu_item_by_id(menu_item_id: int) -> MenuItem | None:
    return next((item for item in MENU_ITEMS if item.id == menu_item_id), None)