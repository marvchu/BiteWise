# User distance

Click **Use my location** and allow the browser's location request. The homepage
and restaurant search show distance to the nearest saved restaurant location.
**Closest** sorts the budget results by distance. **Clear location** removes
distances and returns to price sorting. Location is held in page memory and is
requested again after a full refresh; it is not saved to PostgreSQL or local storage.

Distances use the Haversine formula and are shown in miles. They are straight-line
estimates, not walking distances or travel times. The browser determines the accuracy
of the user's coordinates. Restaurants without locations have an unknown distance
and appear last when sorting by distance.

Geolocation requires a secure context (HTTPS in deployment; localhost works for
development) and browser permission. Denial, timeout, or unsupported geolocation
leaves the meal feed usable without distances.
See [MDN's Geolocation documentation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition).

The `/homepage`, `/restaurants`, and `/menu-items` endpoints accept optional
`latitude` and `longitude` query parameters. Both must be supplied together, within
[-90, 90] and [-180, 180] respectively. Responses add nullable `distance_miles`
fields. Pass `sort=distance_miles` with coordinates to sort by distance.

Example:

```text
/homepage?latitude=37.868367&longitude=-122.258959&sort=distance_miles
```

The coordinates are sent to the API in the request URL, so normal server access logs
may contain them. No external routing service or API key is required.

If a selected budget has no matches, the featured meal still falls back to the
cheapest available meal and is labeled as above budget. The budget list stays empty.
