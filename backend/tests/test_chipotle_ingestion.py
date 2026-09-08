from decimal import Decimal

from ingestion.chipotle import ingest_chipotle, parse_chipotle_payload
from models import MenuItem, Restaurant


def chipotle_payload():
    return {
        "locations": [
            {
                "address": "2234 Shattuck Ave, Berkeley, CA 94704",
                "latitude": 37.8677,
                "longitude": -122.2681,
            }
        ],
        "menu_items": [
            {
                "name": "Chicken Burrito Bowl",
                "description": "A burrito bowl with chicken.",
                "category": "bowl",
                "price": "11.25",
                "price_max": "15.45",
                "calories": 630,
                "calories_max": 1345,
            }
        ],
    }


def test_parse_chipotle_payload_normalizes_values_and_preserves_missing_nutrition():
    snapshot = parse_chipotle_payload(chipotle_payload(), "https://example.com/chipotle.json")

    assert snapshot.menu_items[0].price == Decimal("11.25")
    assert snapshot.menu_items[0].calories_max == 1345
    assert snapshot.locations[0].address.startswith("2234 Shattuck")


def test_ingest_chipotle_is_idempotent(db):
    snapshot = parse_chipotle_payload(chipotle_payload(), "https://example.com/chipotle.json")

    ingest_chipotle(db, snapshot)
    ingest_chipotle(db, snapshot)

    restaurant = db.query(Restaurant).filter(Restaurant.name == "Chipotle").one()
    assert len(db.query(Restaurant).filter(Restaurant.name == "Chipotle").all()) == 1
    assert len(restaurant.locations) == 1
    assert len(db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id).all()) == 1
    assert db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id).one().price_max == Decimal("15.45")


def test_parse_chipotle_payload_requires_menu_items():
    payload = chipotle_payload()
    payload["menu_items"] = []

    try:
        parse_chipotle_payload(payload, "https://example.com/chipotle.json")
    except ValueError as exc:
        assert "at least one menu item" in str(exc)
    else:
        raise AssertionError("expected empty menu payload to be rejected")