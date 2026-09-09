import { useEffect, useState } from 'react'

export function useRestaurantSearch(submittedSearch, budget, coordinates, sort) {
  const [results, setResults] = useState([])
  const [error, setError] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  useEffect(() => {
    if (!submittedSearch) return
    const controller = new AbortController()
    async function search() {
      setIsSearching(true)
      setError('')
      const params = new URLSearchParams({ sort })
      if (submittedSearch.query) params.set('query', submittedSearch.query)
      if (budget) params.set('max_price', budget)
      if (coordinates) {
        params.set('latitude', coordinates.latitude)
        params.set('longitude', coordinates.longitude)
      }
      try {
        const response = await fetch(`/api/restaurants?${params.toString()}`, { signal: controller.signal })
        if (!response.ok) throw new Error('Search request failed')
        setResults(await response.json())
      } catch (requestError) {
        if (requestError.name === 'AbortError') return
        setResults([])
        setError('Could not load restaurant results. Make sure the BiteWise API is running.')
      } finally {
        if (!controller.signal.aborted) {
          setHasSearched(true)
          setIsSearching(false)
        }
      }
    }
    search()
    return () => controller.abort()
  }, [submittedSearch, budget, coordinates, sort])

  return { results, error, isSearching, hasSearched }
}
