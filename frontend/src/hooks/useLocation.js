import { useRef, useState } from 'react'

export function useLocation() {
  const [coordinates, setCoordinates] = useState(null)
  const [isLocating, setIsLocating] = useState(false)
  const [error, setError] = useState('')
  const requestId = useRef(0)

  function requestLocation() {
    const id = ++requestId.current
    setError('')
    if (!window.isSecureContext || !navigator.geolocation) {
      setError('Location needs a supported browser on HTTPS or localhost.')
      return
    }
    setIsLocating(true)
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        if (id !== requestId.current) return
        setCoordinates({ latitude: coords.latitude, longitude: coords.longitude })
        setIsLocating(false)
      },
      (failure) => {
        if (id !== requestId.current) return
        setError(failure.code === 1
          ? 'Location access is blocked. Allow it in your browser’s site settings to see distances.'
          : failure.code === 3
            ? 'Finding your location timed out. Try again.'
            : 'Your location is unavailable. Check location services and try again.')
        setIsLocating(false)
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 60000 },
    )
  }

  function clearLocation() {
    requestId.current += 1
    setCoordinates(null)
    setIsLocating(false)
    setError('')
  }

  return { coordinates, isLocating, error, requestLocation, clearLocation }
}
