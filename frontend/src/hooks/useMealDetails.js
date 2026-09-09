import { useEffect, useState } from 'react'

export function useMealDetails(mealId, coordinates) {
  const [detail, setDetail] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    async function load() {
      setDetail(null)
      setError('')
      setIsLoading(true)
      const params = new URLSearchParams()
      if (coordinates) {
        params.set('latitude', coordinates.latitude)
        params.set('longitude', coordinates.longitude)
      }
      try {
        const response = await fetch(`/api/menu-items/${mealId}?${params}`, { signal: controller.signal })
        if (!response.ok) throw new Error('Could not load this meal. Please try again.')
        setDetail(await response.json())
      } catch (failure) {
        if (failure.name !== 'AbortError') setError(failure.message)
        return
      } finally {
        if (!controller.signal.aborted) setIsLoading(false)
      }

    }
    load()
    return () => controller.abort()
  }, [mealId, coordinates, attempt])

  return { detail, error, isLoading, retry: () => setAttempt(value => value + 1) }
}
