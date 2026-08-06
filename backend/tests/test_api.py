from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_menu_items_returns_items_with_metrics():
    response = client.get("/menu-items")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    assert data[0]["name"] == "Chicken Burrito Bowl"
    assert data[0]["protein_per_dollar"] == 4.74
    assert data[0]["calories_per_dollar"] == 68.42


def test_list_menu_items_filters_and_sorts_query_params():
    response = client.get("/menu-items", params={"max_price": 8, "min_protein": 30, "sort": "price"})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == [
        "Double Cheeseburger",
        "Grilled Chicken Sandwich",
    ]


def test_list_menu_items_rejects_negative_query_params():
    response = client.get("/menu-items", params={"max_price": -1})

    assert response.status_code == 422


def test_list_menu_items_rejects_invalid_sort_key():
    response = client.get("/menu-items", params={"sort": "distance"})

    assert response.status_code == 400
    assert "Invalid sort key" in response.json()["detail"]


def test_get_menu_item_returns_item_by_id():
    response = client.get("/menu-items/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Chicken Burrito Bowl"


def test_get_menu_item_returns_404_for_missing_item():
    response = client.get("/menu-items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Menu item not found"


def test_homepage_returns_ranked_sections():
    response = client.get("/homepage")

    assert response.status_code == 200
    data = response.json()
    assert set(data) == {
        "featured",
        "meals_under_budget",
        "active_deals",
        "free_food_today",
        "best_protein_per_dollar",
        "best_calories_per_dollar",
    }
    assert len(data["best_protein_per_dollar"]) == 5
    assert data["meals_under_budget"][0]["name"] == "Double Cheeseburger"
    assert data["featured"]["name"] == "Double Cheeseburger"
    assert data["active_deals"] == []
    assert data["free_food_today"] == []


def test_homepage_max_price_query_param_controls_meals_under_budget():
    response = client.get("/homepage", params={"max_price": 7})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()["meals_under_budget"]] == ["Double Cheeseburger"]


def test_homepage_rejects_negative_max_price():
    response = client.get("/homepage", params={"max_price": -1})

    assert response.status_code == 422


def test_nutrition_filters_exclude_items_with_missing_nutrition():
    response = client.get("/menu-items", params={"min_calories": 500, "max_calories": 600})

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Veggie Burrito", "Bibimbap"]
