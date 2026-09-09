from math import asin, cos, radians, sin, sqrt


def distance_miles(latitude: float, longitude: float, other_latitude: float, other_longitude: float) -> float:
    """Great-circle distance; this is not walking or driving distance."""
    lat1, lat2 = radians(latitude), radians(other_latitude)
    dlat = lat2 - lat1
    dlon = radians(other_longitude - longitude)
    haversine = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 3958.7613 * 2 * asin(sqrt(min(1.0, max(0.0, haversine))))


def nearest_location(locations, coordinates):
    """Return the nearest branch and distance, or an unknown distance."""
    if not locations:
        return None, None
    if coordinates is None:
        return min(locations, key=lambda location: location.id), None
    candidates = [
        (location, distance_miles(*coordinates, float(location.latitude), float(location.longitude)))
        for location in locations
    ]
    return min(candidates, key=lambda candidate: (candidate[1], candidate[0].id))
