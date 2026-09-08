import importlib.util
from pathlib import Path


def load_seed_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "seed_dev_data.py"
    spec = importlib.util.spec_from_file_location("seed_dev_data", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_seed_data_has_restaurants_locations_and_menu_items():
    seed_module = load_seed_module()

    assert len(seed_module.SEED_RESTAURANTS) == 5
    for restaurant in seed_module.SEED_RESTAURANTS:
        assert restaurant["name"]
        assert restaurant["location"]["address"]
        assert restaurant["location"]["latitude"] is not None
        assert restaurant["location"]["longitude"] is not None
        assert len(restaurant["menu_items"]) >= 1


def test_seed_menu_items_have_required_fields():
    seed_module = load_seed_module()

    for restaurant in seed_module.SEED_RESTAURANTS:
        for item in restaurant["menu_items"]:
            assert item["name"]
            assert item["category"]
            assert item["price"] > 0
            assert "calories" in item
