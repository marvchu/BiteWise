from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import app
from db.session import get_db
from models import Location, Restaurant
from services.distance import distance_miles


@pytest.fixture
def client(db):
    previous = app.dependency_overrides[get_db]
    app.dependency_overrides[get_db] = lambda: db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides[get_db] = previous


def test_distance_known_points_and_wraparound():
    assert distance_miles(0, 0, 0, 0) == 0
    assert distance_miles(0, 0, 0, 1) == pytest.approx(69.0934, abs=0.001)
    assert distance_miles(0, 179, 0, -179) == pytest.approx(138.1868, abs=0.001)
    assert distance_miles(0, 0, 0, 180) == pytest.approx(12436.815, abs=0.01)


@pytest.mark.parametrize('endpoint', ['/homepage', '/restaurants', '/menu-items'])
@pytest.mark.parametrize('params', [
    {'latitude': 37}, {'longitude': -122},
    {'latitude': 91, 'longitude': 0}, {'latitude': 0, 'longitude': -181},
    {'latitude': 'nan', 'longitude': 0}, {'latitude': 0, 'longitude': 'inf'},
])
def test_invalid_coordinates_are_rejected(client, endpoint, params):
    assert client.get(endpoint, params=params).status_code == 422


def test_homepage_without_location_keeps_meals_and_unknown_distance(client):
    data = client.get('/homepage').json()
    assert data['featured'] is not None
    assert data['featured']['distance_miles'] is None


def test_closest_sort_and_budget_fallback(client):
    params = {'latitude': 37.868, 'longitude': -122.256, 'sort': 'distance_miles'}
    data = client.get('/homepage', params=params).json()
    assert data['featured']['restaurant_name'] == 'Bancroft Korean'
    assert data['featured']['distance_miles'] == 0
    distances = [meal['distance_miles'] for meal in data['meals_under_budget']]
    assert distances == sorted(distances)
    fallback = client.get('/homepage', params={**params, 'max_price': 5}).json()
    assert fallback['featured']['name'] == 'Double Cheeseburger'
    assert fallback['featured']['distance_miles'] > 0
    assert fallback['meals_under_budget'] == []


def test_nearest_branch_address_and_missing_locations(client, db):
    restaurant = db.get(Restaurant, 1)
    restaurant.locations.append(Location(
        address='Nearest branch', latitude=Decimal('0'), longitude=Decimal('0'),
    ))
    restaurant_without_location = db.get(Restaurant, 2)
    restaurant_without_location.locations.clear()
    db.commit()
    params = {'latitude': 0, 'longitude': 0, 'sort': 'distance_miles'}
    response = client.get('/restaurants', params=params)
    assert response.status_code == 200
    results = response.json()
    assert results[0]['id'] == 1
    assert results[0]['address'] == 'Nearest branch'
    assert results[0]['distance_miles'] == 0
    assert all(item['distance_miles'] == 0 for item in results[0]['matching_items'])
    assert results[-1]['id'] == 2
    assert results[-1]['distance_miles'] is None
    meals = client.get('/menu-items', params=params).json()
    assert meals[0]['restaurant_id'] == 1
    assert meals[-1]['distance_miles'] is None


@pytest.mark.parametrize('endpoint', ['/homepage', '/restaurants'])
def test_closest_sort_requires_location(client, endpoint):
    assert client.get(endpoint, params={'sort': 'distance_miles'}).status_code == 422
