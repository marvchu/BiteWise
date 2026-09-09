export function Distance({ miles }) {
  if (miles === null || miles === undefined) return null
  return <span className="distance">{miles < 0.1 ? '<0.1' : miles.toFixed(1)} mi away · straight-line</span>
}
