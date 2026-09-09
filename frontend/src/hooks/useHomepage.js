import { useEffect, useState } from 'react'

export function useHomepage(budget, coordinates, sort = 'price') {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [requestVersion, setRequestVersion] = useState(0)

  useEffect(() => {
    const controller = new AbortController()

    async function loadHomepage() {
      setIsLoading(true)
      setError('')

      const params = new URLSearchParams()
      if (budget) params.set('max_price', budget)
      params.set('sort', sort)
      if (coordinates) {
        params.set('latitude', coordinates.latitude)
        params.set('longitude', coordinates.longitude)
      }

      try {
        const response = await fetch(`/api/homepage?${params.toString()}`, {
          signal: controller.signal,
        })
        if (!response.ok) throw new Error('Homepage request failed')
        setData(await response.json())
      } catch (requestError) {
        if (requestError.name !== 'AbortError') {
          setData(null)
          setError('Could not load recommendations. Make sure the BiteWise API is running.')
        }
      } finally {
        if (!controller.signal.aborted) setIsLoading(false)
      }
    }

    loadHomepage()
    return () => controller.abort()
  }, [budget, coordinates, sort, requestVersion])

  return {
    data,
    error,
    isLoading,
    retry: () => setRequestVersion((current) => current + 1),
  }
}
