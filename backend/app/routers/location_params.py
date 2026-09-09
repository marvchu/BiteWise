from fastapi import HTTPException, Query


def user_coordinates(
    latitude: float | None = Query(default=None, ge=-90, le=90),
    longitude: float | None = Query(default=None, ge=-180, le=180),
) -> tuple[float, float] | None:
    if (latitude is None) != (longitude is None):
        raise HTTPException(status_code=422, detail="Provide both latitude and longitude")
    return (latitude, longitude) if latitude is not None else None
