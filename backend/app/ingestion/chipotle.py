"""Chipotle menu ingestion from an exported or API JSON payload.

The external payload is intentionally kept outside the database model. Chipotle
can change its response shape without forcing changes to the rest of BiteWise.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from sqlalchemy.orm import Session

from models.location import Location
from models.menu_item import MenuItem
from models.restaurant import Restaurant

CHIPOTLE_NAME = "Chipotle"
CHIPOTLE_WEBSITE = "https://www.chipotle.com/"


@dataclass(frozen=True)
class ChipotleLocation:
    address: str
    latitude: Decimal
    longitude: Decimal


@dataclass(frozen=True)
class ChipotleMenuItem:
    name: str
    description: str | None
    category: str | None
    price: Decimal
    price_max: Decimal | None
    calories: int | None
    calories_max: int | None


@dataclass(frozen=True)
class ChipotleSnapshot:
    source_url: str
    locations: tuple[ChipotleLocation, ...]
    menu_items: tuple[ChipotleMenuItem, ...]


def _required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Chipotle payload field '{field}' must be a non-empty string")
    return value.strip()


def _decimal(value: Any, field: str, required: bool = True) -> Decimal | None:
    if value is None and not required:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"Chipotle payload field '{field}' must be numeric") from exc


def _optional_string(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def parse_chipotle_payload(payload: dict[str, Any], source_url: str) -> ChipotleSnapshot:
    """Validate and normalize the supported Chipotle JSON export format.

    Expected top-level keys are ``locations`` and ``menu_items``. Nutrition is
    optional and remains null when the source does not provide it.
    """
    if not isinstance(payload, dict):
        raise ValueError("Chipotle payload must be a JSON object")
    locations = payload.get("locations", [])
    menu_items = payload.get("menu_items", [])
    if not isinstance(locations, list) or not isinstance(menu_items, list):
        raise ValueError("Chipotle payload locations and menu_items must be arrays")
    if not menu_items:
        raise ValueError("Chipotle payload must contain at least one menu item")

    normalized_locations = tuple(
        ChipotleLocation(
            address=_required_string(item.get("address"), "locations[].address"),
            latitude=_decimal(item.get("latitude"), "locations[].latitude"),
            longitude=_decimal(item.get("longitude"), "locations[].longitude"),
        )
        for item in locations
    )
    normalized_items = tuple(
        ChipotleMenuItem(
            name=_required_string(item.get("name"), "menu_items[].name"),
            description=_optional_string(item.get("description")),
            category=_optional_string(item.get("category")),
            price=_decimal(item.get("price"), "menu_items[].price"),
            price_max=_decimal(item.get("price_max"), "menu_items[].price_max", required=False),
            calories=int(item["calories"]) if item.get("calories") is not None else None,
            calories_max=int(item["calories_max"]) if item.get("calories_max") is not None else None,
        )
        for item in menu_items
    )
    return ChipotleSnapshot(
        source_url=_required_string(source_url, "source_url"),
        locations=normalized_locations,
        menu_items=normalized_items,
    )


def ingest_chipotle(db: Session, snapshot: ChipotleSnapshot) -> tuple[Restaurant, int]:
    """Upsert one Chipotle snapshot and return the restaurant and item count."""
    restaurant = db.query(Restaurant).filter(Restaurant.name == CHIPOTLE_NAME).one_or_none()
    if restaurant is None:
        restaurant = Restaurant(name=CHIPOTLE_NAME)
        db.add(restaurant)
        db.flush()

    restaurant.website_url = CHIPOTLE_WEBSITE
    restaurant.source_url = snapshot.source_url

    existing_locations = {location.address: location for location in restaurant.locations}
    for location_data in snapshot.locations:
        location = existing_locations.get(location_data.address)
        if location is None:
            location = Location(restaurant_id=restaurant.id, address=location_data.address)
            restaurant.locations.append(location)
        location.latitude = location_data.latitude
        location.longitude = location_data.longitude

    existing_items = {item.name.casefold(): item for item in restaurant.menu_items}
    for item_data in snapshot.menu_items:
        item = existing_items.get(item_data.name.casefold())
        if item is None:
            item = MenuItem(restaurant_id=restaurant.id, name=item_data.name)
            restaurant.menu_items.append(item)
        item.description = item_data.description
        item.category = item_data.category
        item.price = item_data.price
        item.price_max = item_data.price_max
        item.calories = item_data.calories
        item.calories_max = item_data.calories_max
        item.source_url = snapshot.source_url

    db.commit()
    db.refresh(restaurant)
    return restaurant, len(snapshot.menu_items)