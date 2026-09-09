export function LocationSelector({ location }) {
  return (
    <div className="location-controls">
      <button className="location" type="button" onClick={location.requestLocation} disabled={location.isLocating}>
        {location.isLocating ? 'Finding location…' : location.coordinates ? 'Update my location' : 'Use my location'}
      </button>
      {location.coordinates ? (
        <button className="chip" type="button" onClick={location.clearLocation}>Clear location</button>
      ) : null}
    </div>
  )
}
