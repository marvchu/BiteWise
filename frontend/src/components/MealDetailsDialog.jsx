import { useEffect, useRef } from 'react'
import { useMealDetails } from '../hooks/useMealDetails.js'
import { RestaurantMap } from './RestaurantMap.jsx'
import './MealDetailsDialog.css'

export function MealDetailsDialog({ meal, location, onClose }) {
  const dialogRef = useRef(null)
  const closeRef = useRef(null)
  const { detail, error, isLoading, retry } = useMealDetails(meal.id, location.coordinates)
  const current = detail || meal
  const destination = detail?.location

  useEffect(() => {
    const dialog = dialogRef.current
    const previousFocus = document.activeElement
    const previousOverflow = document.body.style.overflow
    dialog.showModal()
    closeRef.current.focus()
    document.body.style.overflow = 'hidden'
    return () => {
      dialog.close()
      document.body.style.overflow = previousOverflow
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus()
      else document.querySelector(`[data-meal-detail="${meal.id}"]`)?.focus()
    }
  }, [meal.id])

  return (
    <dialog ref={dialogRef} className="meal-dialog" aria-labelledby="meal-dialog-title"
      onCancel={event => { event.preventDefault(); onClose() }}
      onClick={event => { if (event.target === event.currentTarget) onClose() }}>
      <div className="meal-dialog-content">
        <header className="meal-dialog-header">
          <div>
            <p className="meal-dialog-eyebrow">Your next bite</p>
            <h2 id="meal-dialog-title">{current.name}</h2>
            <p>{current.restaurant_name}</p>
          </div>
          <button ref={closeRef} className="meal-dialog-close" type="button" onClick={onClose} aria-label="Close meal details">×</button>
        </header>
        {destination ? (
          <RestaurantMap destination={destination} coordinates={location.coordinates} restaurantName={current.restaurant_name} />
        ) : (
          <div className="meal-map-placeholder" role="status">
            {isLoading ? 'Loading restaurant map…' : error || 'A map location is not available for this restaurant yet.'}
          </div>
        )}
        <div className="meal-dialog-body">
          <div className="meal-dialog-summary">
            <div className="meal-dialog-cost">
              <strong>{new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(current.price)}</strong>
              <span>meal price</span>
            </div>
            {detail?.distance_miles != null ? (
              <div className="map-distance-summary">
                <strong>{detail.distance_miles < 0.1 ? '<0.1' : detail.distance_miles.toFixed(1)} mi</strong>
                <span>straight-line distance</span>
              </div>
            ) : null}
          </div>
          {destination ? (
            <div className="map-destination">
              <span className="map-key map-key-destination" aria-hidden="true" />
              <div><strong>{current.restaurant_name}</strong><p>{destination.address}</p></div>
            </div>
          ) : null}
          {location.coordinates && destination ? (
            <p className="map-origin"><span className="map-key map-key-origin" aria-hidden="true" />Your current location</p>
          ) : null}
          <div className="meal-map-status" role="status">
            {location.error ? <p>{location.error}</p> : null}
            {!location.coordinates && destination ? <p>Use your location to see where you are relative to the restaurant.</p> : null}
          </div>
          <div className="meal-dialog-actions">
            {!location.coordinates && destination ? (
              <button className="map-primary" type="button" onClick={location.requestLocation} disabled={location.isLocating}>
                {location.isLocating ? 'Finding location…' : 'Use my location'}
              </button>
            ) : null}
            {error ? <button className="map-secondary" type="button" onClick={retry}>Try again</button> : null}

          </div>
        </div>
      </div>
    </dialog>
  )
}
