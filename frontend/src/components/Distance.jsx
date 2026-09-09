import { formatEstimatedWalkingDistance, formatEstimatedWalkingTime } from '../utils/distance.js'

export function Distance({ miles }) {
  const distance = formatEstimatedWalkingDistance(miles)
  if (distance === null) return null
  return <span className="distance">Est. {formatEstimatedWalkingTime(miles)} walk · {distance}</span>
}
