# Restaurant map popup

**View details** opens a Leaflet map with OpenStreetMap tiles and a restaurant pin.
Allow browser location to add your position and see straight-line distance. No
routing provider or API key is needed for this setup. The popup does not request
walking routes or show walking times.

The popup is a bottom sheet on mobile and a centered dialog on desktop. Escape,
the close button, or clicking outside dismisses it and restores focus. Missing
locations, blocked location access, and tile errors have explicit UI states.

`GET /menu-items/{id}` accepts an optional latitude/longitude pair and returns the
nearest saved restaurant branch as `location`. Browser location is not stored in
PostgreSQL. Tiles are requested directly by the browser only while the map is open.

Install frontend dependencies with `npm --prefix frontend ci`. To change tile
providers, configure `VITE_MAP_TILE_URL` and `VITE_MAP_ATTRIBUTION` and restart Vite
or rebuild. The default URL is `https://tile.openstreetmap.org/{z}/{x}/{y}.png`.
Visible attribution and browser caching are preserved; tiles are not prefetched.
See the [OSM tile usage policy](https://operations.osmfoundation.org/policies/tiles/).
