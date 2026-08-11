import sys
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from db.base import Base  # noqa: E402
from db.session import get_db  # noqa: E402
from app.main import app as package_app  # noqa: E402
from main import app as top_level_app  # noqa: E402
from models import Location, MenuItem, Restaurant  # noqa: E402


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def seed_test_data(db):
    db.execute(delete(MenuItem))
    db.execute(delete(Location))
    db.execute(delete(Restaurant))

    restaurants = [
        Restaurant(id=1, name="Telegraph Taqueria"),
        Restaurant(id=2, name="Campus Cafe"),
        Restaurant(id=3, name="Bancroft Korean"),
    ]
    restaurants[0].locations.append(
        Location(
            address="Telegraph Avenue, Berkeley",
            latitude=Decimal("37.865000"),
            longitude=Decimal("-122.258000"),
        )
    )
    restaurants[1].locations.append(
        Location(
            address="Bancroft Way, Berkeley",
            latitude=Decimal("37.867000"),
            longitude=Decimal("-122.257000"),
        )
    )
    restaurants[2].locations.append(
        Location(
            address="Bancroft Way, Berkeley",
            latitude=Decimal("37.868000"),
            longitude=Decimal("-122.256000"),
        )
    )

    menu_items = [
        MenuItem(id=1, restaurant_id=1, name="Chicken Burrito Bowl", price=Decimal("9.50"), category="bowl", protein_grams=Decimal("45.00"), calories=650),
        MenuItem(id=2, restaurant_id=1, name="Veggie Burrito", price=Decimal("8.00"), category="burrito", protein_grams=Decimal("15.00"), calories=550),
        MenuItem(id=3, restaurant_id=2, name="Double Cheeseburger", price=Decimal("6.50"), category="burger", protein_grams=Decimal("35.00"), calories=780),
        MenuItem(id=4, restaurant_id=2, name="Grilled Chicken Sandwich", price=Decimal("7.25"), category="sandwich", protein_grams=Decimal("38.00"), calories=520),
        MenuItem(id=5, restaurant_id=3, name="Bibimbap", price=Decimal("11.00"), category="rice", protein_grams=Decimal("28.00"), calories=600),
        MenuItem(id=6, restaurant_id=3, name="Ramen", price=Decimal("10.50"), category="noodles", protein_grams=None, calories=None),
    ]

    db.add_all(restaurants)
    db.flush()
    db.add_all(menu_items)
    db.commit()


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    seed_test_data(session)
    try:
        yield session
    finally:
        session.close()


def override_get_db():
    session = TestingSessionLocal()
    seed_test_data(session)
    try:
        yield session
    finally:
        session.close()


package_app.dependency_overrides[get_db] = override_get_db
top_level_app.dependency_overrides[get_db] = override_get_db
