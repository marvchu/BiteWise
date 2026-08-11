from decimal import Decimal
from pathlib import Path
import sys

from sqlalchemy import delete

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from db.base import Base  # noqa: E402
from db.session import engine, SessionLocal  # noqa: E402
from models import Location, MenuItem, Restaurant  # noqa: E402


# Development seed data only.
# Restaurant names are real Berkeley-area examples, but menu items, prices,
# nutrition, and coordinates should be treated as approximate/unverified.
SEED_RESTAURANTS = [
    {
        "id": 1,
        "name": "Mezzo",
        "website_url": "https://www.mezzo-berkeley.com/",
        "source_url": "https://www.mezzo-berkeley.com/",
        "location": {
            "address": "2442 Telegraph Ave, Berkeley, CA 94704",
            "latitude": Decimal("37.865860"),
            "longitude": Decimal("-122.258090"),
        },
        "menu_items": [
            {
                "name": "Half Sandwich",
                "description": "Development sample sandwich option.",
                "category": "sandwich",
                "price": Decimal("8.95"),
                "protein_grams": None,
                "calories": None,
            },
            {
                "name": "Salad Bowl",
                "description": "Development sample salad option.",
                "category": "salad",
                "price": Decimal("10.50"),
                "protein_grams": None,
                "calories": None,
            },
        ],
    },
    {
        "id": 2,
        "name": "Top Dog",
        "website_url": "https://topdoghotdogs.com/",
        "source_url": "https://topdoghotdogs.com/",
        "location": {
            "address": "2534 Durant Ave, Berkeley, CA 94704",
            "latitude": Decimal("37.867040"),
            "longitude": Decimal("-122.257300"),
        },
        "menu_items": [
            {
                "name": "Hot Dog",
                "description": "Development sample classic hot dog.",
                "category": "sandwich",
                "price": Decimal("5.75"),
                "protein_grams": Decimal("14.00"),
                "calories": 320,
            },
            {
                "name": "Chicken Apple Sausage",
                "description": "Development sample sausage option.",
                "category": "sandwich",
                "price": Decimal("6.50"),
                "protein_grams": Decimal("16.00"),
                "calories": 360,
            },
        ],
    },
    {
        "id": 3,
        "name": "La Burrita",
        "website_url": None,
        "source_url": None,
        "location": {
            "address": "2530 Durant Ave, Berkeley, CA 94704",
            "latitude": Decimal("37.867080"),
            "longitude": Decimal("-122.257560"),
        },
        "menu_items": [
            {
                "name": "Bean and Cheese Burrito",
                "description": "Development sample burrito option.",
                "category": "burrito",
                "price": Decimal("8.25"),
                "protein_grams": Decimal("18.00"),
                "calories": 620,
            },
            {
                "name": "Chicken Burrito",
                "description": "Development sample chicken burrito.",
                "category": "burrito",
                "price": Decimal("10.75"),
                "protein_grams": Decimal("35.00"),
                "calories": 760,
            },
        ],
    },
    {
        "id": 4,
        "name": "Gypsy's Trattoria Italiana",
        "website_url": "https://gypsystrattoria.com/",
        "source_url": "https://gypsystrattoria.com/",
        "location": {
            "address": "2519 Durant Ave, Berkeley, CA 94704",
            "latitude": Decimal("37.867210"),
            "longitude": Decimal("-122.258410"),
        },
        "menu_items": [
            {
                "name": "Pasta Marinara",
                "description": "Development sample pasta option.",
                "category": "pasta",
                "price": Decimal("9.95"),
                "protein_grams": Decimal("14.00"),
                "calories": 680,
            },
            {
                "name": "Chicken Alfredo",
                "description": "Development sample chicken pasta.",
                "category": "pasta",
                "price": Decimal("12.95"),
                "protein_grams": Decimal("32.00"),
                "calories": 920,
            },
        ],
    },
    {
        "id": 5,
        "name": "Asian Ghetto Thai",
        "website_url": None,
        "source_url": None,
        "location": {
            "address": "Durant Ave, Berkeley, CA 94704",
            "latitude": Decimal("37.867230"),
            "longitude": Decimal("-122.257920"),
        },
        "menu_items": [
            {
                "name": "Pad Thai",
                "description": "Development sample noodle option.",
                "category": "noodles",
                "price": Decimal("11.50"),
                "protein_grams": Decimal("22.00"),
                "calories": 780,
            },
            {
                "name": "Basil Chicken Rice Plate",
                "description": "Development sample rice plate.",
                "category": "rice",
                "price": Decimal("10.95"),
                "protein_grams": Decimal("30.00"),
                "calories": 720,
            },
        ],
    },
]


def reset_seed_data() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        db.execute(delete(MenuItem))
        db.execute(delete(Location))
        db.execute(delete(Restaurant))

        item_count = 0
        for restaurant_data in SEED_RESTAURANTS:
            location_data = restaurant_data["location"]
            menu_items = restaurant_data["menu_items"]
            restaurant = Restaurant(
                id=restaurant_data["id"],
                name=restaurant_data["name"],
                website_url=restaurant_data["website_url"],
                source_url=restaurant_data["source_url"],
            )
            restaurant.locations.append(Location(**location_data))
            for item_data in menu_items:
                restaurant.menu_items.append(
                    MenuItem(
                        **item_data,
                        source_url=restaurant_data["source_url"],
                    )
                )
                item_count += 1

            db.add(restaurant)

        db.commit()

    print("Seeded development data.")
    print("Data is approximate and unverified; do not present it as production truth.")
    print(f"Restaurants: {len(SEED_RESTAURANTS)}")
    print(f"Menu items: {item_count}")


if __name__ == "__main__":
    reset_seed_data()
