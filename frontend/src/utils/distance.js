// A rough allowance for indirect streets; no walking route is calculated.
const WALKING_DISTANCE_FACTOR = 1.3
const METERS_PER_MILE = 1609.344
const WALKING_METERS_PER_MINUTE = 80

export function formatEstimatedWalkingTime(straightLineMiles) {
  if (!Number.isFinite(straightLineMiles) || straightLineMiles < 0) return null
  const minutes = straightLineMiles * WALKING_DISTANCE_FACTOR * METERS_PER_MILE / WALKING_METERS_PER_MINUTE
  return minutes < 1 ? '<1 min' : `${Math.round(minutes)} min`
}

export function formatEstimatedWalkingDistance(straightLineMiles) {
  if (!Number.isFinite(straightLineMiles) || straightLineMiles < 0) return null
  const miles = straightLineMiles * WALKING_DISTANCE_FACTOR
  return `${miles === 0 ? '0' : miles < 0.1 ? '<0.1' : miles.toFixed(1)} mi`
}
