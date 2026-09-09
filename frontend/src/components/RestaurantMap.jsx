import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

function label(text) {
  const element = document.createElement('span')
  element.textContent = text
  return element
}

export function RestaurantMap({ destination, coordinates, restaurantName }) {
  const container = useRef(null)
  const mapRef = useRef(null)
  const tilesRef = useRef(null)
  const [tileError, setTileError] = useState(false)

  useEffect(() => {
    const map = L.map(container.current, { zoomControl: false, scrollWheelZoom: false })
    mapRef.current = map
    L.control.zoom({ position: 'bottomright' }).addTo(map)
    const tiles = L.tileLayer(import.meta.env.VITE_MAP_TILE_URL || 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: import.meta.env.VITE_MAP_ATTRIBUTION || '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)
    tilesRef.current = tiles
    tiles.on('tileerror', () => setTileError(true))
    const observer = new ResizeObserver(() => map.invalidateSize())
    observer.observe(container.current)
    return () => {
      observer.disconnect()
      map.remove()
      mapRef.current = null
    }
  }, [])

  useEffect(() => {
    const map = mapRef.current
    if (!map || !destination) return
    const group = L.featureGroup().addTo(map)
    const destinationPoint = [destination.latitude, destination.longitude]
    const bounds = L.latLngBounds([destinationPoint])
    if (coordinates) {
      const origin = [coordinates.latitude, coordinates.longitude]
      L.circleMarker(origin, { radius: 8, color: '#ffffff', weight: 3, fillColor: '#202820', fillOpacity: 1 })
        .bindTooltip(label('You'), { direction: 'top' }).addTo(group)
      bounds.extend(origin)
    }
    L.circleMarker(destinationPoint, { radius: 11, color: '#ffffff', weight: 3, fillColor: '#237a43', fillOpacity: 1 })
      .bindTooltip(label(restaurantName), { direction: 'top' }).addTo(group)
    map.fitBounds(bounds, {
      paddingTopLeft: [40, 40], paddingBottomRight: [76, 104], maxZoom: 16, animate: false,
    })
    return () => group.remove()
  }, [destination, coordinates, restaurantName])

  return (
    <div className="restaurant-map-wrap">
      <div ref={container} className="restaurant-map" role="region" aria-label={`Map of ${restaurantName}`} />
      {tileError ? (
        <div className="map-tile-error" role="status">
          Some map tiles could not load.
          <button type="button" onClick={() => { setTileError(false); tilesRef.current?.redraw() }}>Retry map</button>
        </div>
      ) : null}
    </div>
  )
}
