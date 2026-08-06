from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_restaurants_matches_food_and_budget():
    response = client.get("/restaurants", params={"query": "burrito", "max_price": 9})

    assert response.status_code == 200
    data = response.json()
    assert [restaurant["name"] for restaurant in data] == ["Telegraph Taqueria"]
    assert [item["name"] for item in data[0]["matching_items"]] == ["Veggie Burrito"]
    assert data[0]["lowest_matching_price"] == 8.0


def test_search_restaurants_excludes_restaurants_without_qualifying_items():
    response = client.get("/restaurants", params={"query": "chicken", "max_price": 7})

    assert response.status_code == 200
    assert response.json() == []


def test_search_restaurants_matches_manual_food_category():
    response = client.get("/restaurants", params={"query": "noodles", "max_price": 12})

    assert response.status_code == 200
    assert response.json()[0]["matching_items"][0]["name"] == "Ramen"


def test_list_restaurants_without_query_returns_affordable_matches():
    response = client.get("/restaurants", params={"max_price": 7})

    assert response.status_code == 200
    assert [restaurant["name"] for restaurant in response.json()] == ["Campus Cafe"]


def test_get_restaurant_returns_its_menu():
    response = client.get("/restaurants/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Telegraph Taqueria"
    assert len(response.json()["menu_items"]) == 2


def test_get_restaurant_returns_404_for_missing_restaurant():
    response = client.get("/restaurants/999")

    assert response.status_code == 404
