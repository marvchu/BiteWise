import { useState } from 'react'
import './App.css'
import { useHomepage } from './hooks/useHomepage.js'
import { useLocation } from './hooks/useLocation.js'
import { useRestaurantSearch } from './hooks/useRestaurantSearch.js'
import { LocationSelector } from './components/LocationSelector.jsx'
import { Distance } from './components/Distance.jsx'
import { MealDetailsDialog } from './components/MealDetailsDialog.jsx'

const budgetOptions = [5, 10, 15, 20]

function formatPrice(price) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(price)
}

function Header({ isDarkMode, onToggleTheme, location }) {
  return (
    <header className="app-header">
      <a className="brand" href="/" aria-label="BiteWise home">
        BiteWise
      </a>
      <div className="header-actions">
        <button
          className="theme-toggle"
          type="button"
          aria-pressed={isDarkMode}
          onClick={onToggleTheme}
        >
          <span>{isDarkMode ? 'Light' : 'Dark'}</span>
        </button>
        <LocationSelector location={location} />
      </div>
    </header>
  )
}

function SearchBar({ budget, query, isSearching, onBudgetChange, onQueryChange, onSubmit }) {
  return (
    <form className="search" role="search" onSubmit={onSubmit}>
      <label htmlFor="meal-search">Find meals</label>
      <div className="search-row">
        <input
          id="meal-search"
          type="search"
          placeholder="Search burritos, bowls, burgers"
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
        />
        <label className="budget-control" htmlFor="meal-budget">
          <span>Budget</span>
          <select
            id="meal-budget"
            value={budget}
            onChange={(event) => onBudgetChange(event.target.value)}
          >
            {budgetOptions.map((amount) => (
              <option value={amount} key={amount}>Under ${amount}</option>
            ))}
            <option value="">Any price</option>
          </select>
        </label>
        <button type="submit" disabled={isSearching}>
          {isSearching ? 'Searching...' : 'Search'}
        </button>
      </div>
    </form>
  )
}

function FilterChips({ sort, onSortChange, hasLocation }) {
  return (
    <div className="filter-strip" aria-label="Meal filters">
      {[['price', 'Lowest price'], ['distance_miles', 'Closest']].map(([value, label]) => (
        <button className={`chip${sort === value ? ' active' : ''}`} type="button" key={value}
          aria-pressed={sort === value} onClick={() => onSortChange(value)}
          disabled={value === 'distance_miles' && !hasLocation}>
          {label}
        </button>
      ))}
    </div>
  )
}

function RestaurantResults({ query, results, error, hasSearched, onViewDetails }) {
  if (!hasSearched) return null

  return (
    <section className="search-results" aria-labelledby="search-results-title">
      <div className="section-heading">
        <h2 id="search-results-title">
          {query ? `Restaurants with “${query}”` : 'Restaurants within your budget'}
        </h2>
      </div>
      {error ? <div className="empty-state" role="alert">{error}</div> : null}
      {!error && results.length === 0 ? (
        <div className="empty-state">No restaurants have a matching meal within this budget.</div>
      ) : null}
      {!error && results.length > 0 ? (
        <div className="restaurant-results-grid">
          {results.map((restaurant) => (
            <article className="restaurant-result" key={restaurant.id}>
              <div>
                <h3>{restaurant.name}</h3>
                {restaurant.address ? <p>{restaurant.address}</p> : null}
                <Distance miles={restaurant.distance_miles} />
              </div>
              <strong className="result-price">
                From {formatPrice(restaurant.lowest_matching_price)}
              </strong>
              <div className="matching-items">
                {restaurant.matching_items.map((item) => (
                  <div className="matching-item" key={item.id}>
                    <button className="details-button" type="button" data-meal-detail={item.id} onClick={() => onViewDetails(item)} aria-label={`View ${item.name} details`}>{item.name}</button>
                    <strong>{formatPrice(item.price)}</strong>
                  </div>
                ))}
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  )
}

function FeaturedMetric({ label, value }) {
  if (value === null || value === undefined) {
    return null
  }

  return (
    <div className="featured-metric">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  )
}

function FeaturedMeal({ meal, budget, sort, onViewDetails }) {
  return (
    <section className="featured" aria-labelledby="featured-title">
      <div className="featured-copy">
        <p className="featured-label">Best option right now</p>
        {budget && meal.price > Number(budget) ? (
          <p>Lowest available price — above your ${budget} budget.</p>
        ) : null}
        <div className="featured-title-row">
          <h1 id="featured-title">{meal.name}</h1>
          <span className="featured-reason">{sort === 'distance_miles' && meal.distance_miles != null && !(budget && meal.price > Number(budget)) ? 'Closest' : 'Best price'}</span>
        </div>
        <p className="featured-meta">
          {meal.restaurant_name}
        </p>
        <Distance miles={meal.distance_miles} />
        <div className="featured-metrics" aria-label="Featured meal metrics">
          <FeaturedMetric label="calories per dollar" value={meal.calories_per_dollar} />
          <FeaturedMetric
            label="calories"
            value={meal.calories === null ? null : `${meal.calories} cal`}
          />
        </div>
      </div>
      <div className="featured-action">
        <span className="featured-price">{formatPrice(meal.price)}</span>
        <span className="featured-price-label">total price</span>
        <button type="button" data-meal-detail={meal.id} onClick={() => onViewDetails(meal)}>View details</button>
      </div>
    </section>
  )
}

function MealMetric({ label, value }) {
  if (value === null || value === undefined) {
    return null
  }

  return (
    <div className="metric">
      <span>{value}</span>
      <small>{label}</small>
    </div>
  )
}

function MealCard({ meal, reason, onViewDetails }) {
  const badge = reason === null ? null : reason || meal.badge
  return (
    <article className="meal-card">
      <div className="meal-card-top">
        <div className="meal-identity">
          <h3>{meal.name}</h3>
          <p>
            {meal.restaurant_name}
          </p>
          <Distance miles={meal.distance_miles} />
        </div>
        <strong className="meal-price">{formatPrice(meal.price)}</strong>
      </div>
      <div className="meal-support">
        {badge ? <span className="badge subtle">{badge}</span> : null}
        <div className="meal-metrics">
          <MealMetric
            label="calories"
            value={meal.calories === null ? null : `${meal.calories} cal`}
          />
          <MealMetric label="calories/$" value={meal.calories_per_dollar} />
        </div>
      </div>
      <button className="details-button" type="button" data-meal-detail={meal.id} onClick={() => onViewDetails(meal)} aria-label={`View ${meal.name} details`}>
        View details
      </button>
    </article>
  )
}

function MealSection({ title, meals, reason, onViewDetails }) {
  if (meals.length === 0) {
    return (
      <section className="meal-section" aria-labelledby={`${title.replaceAll(' ', '-')}-title`}>
        <div className="section-heading">
          <div>
            <h2 id={`${title.replaceAll(' ', '-')}-title`}>{title}</h2>
          </div>
        </div>
        <div className="empty-state">No meals match this section yet.</div>
      </section>
    )
  }

  return (
    <section className="meal-section" aria-labelledby={`${title.replaceAll(' ', '-')}-title`}>
      <div className="section-heading">
        <div>
          <h2 id={`${title.replaceAll(' ', '-')}-title`}>{title}</h2>
        </div>
      </div>
      <div className="meal-grid">
        {meals.map((meal) => (
          <MealCard meal={meal} reason={reason} onViewDetails={onViewDetails} key={`${title}-${meal.id}`} />
        ))}
      </div>
    </section>
  )
}

function App() {
  const [selectedMeal, setSelectedMeal] = useState(null)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [query, setQuery] = useState('')
  const [budget, setBudget] = useState('')
  const location = useLocation()
  const [selectedSort, setSelectedSort] = useState('price')
  const sort = location.coordinates ? selectedSort : 'price'
  const [submittedSearch, setSubmittedSearch] = useState(null)
  const { results: searchResults, error: searchError, isSearching, hasSearched } =
    useRestaurantSearch(submittedSearch, budget, location.coordinates, sort)
  const {
    data: homepageData,
    error: homepageError,
    isLoading: isHomepageLoading,
    retry: retryHomepage,
  } = useHomepage(budget, location.coordinates, sort)

  function handleSearch(event) {
    event.preventDefault()
    setSubmittedSearch({ query: query.trim() })
  }


  return (
    <div className="app-theme" data-theme={isDarkMode ? 'dark' : 'light'}>
      <main className="app-shell">
        <Header
          isDarkMode={isDarkMode}
          onToggleTheme={() => setIsDarkMode((current) => !current)}
          location={location}
        />
        <section className="hero-panel">
          <SearchBar
            budget={budget}
            query={query}
            isSearching={isSearching}
            onBudgetChange={setBudget}
            onQueryChange={setQuery}
            onSubmit={handleSearch}
          />
          <FilterChips sort={sort} onSortChange={setSelectedSort} hasLocation={Boolean(location.coordinates)} />
          <p className="location-status" role="status">
            {location.error || (location.isLocating ? 'Waiting for your browser location…' : location.coordinates
              ? 'Walking estimates use 1.3× straight-line distance and a pace of 80 meters per minute. Actual routes and times may vary.'
              : 'Use my location to see distances and sort by closest.')}
          </p>
          {isHomepageLoading ? (
            <div className="empty-state" role="status">Loading recommendations...</div>
          ) : null}
          {homepageError ? (
            <div className="empty-state" role="alert">
              <p>{homepageError}</p>
              <button type="button" onClick={retryHomepage}>Try again</button>
            </div>
          ) : null}
          {!isHomepageLoading && !homepageError && homepageData?.featured ? (
            <FeaturedMeal meal={homepageData.featured} budget={budget} sort={sort} onViewDetails={setSelectedMeal} />
          ) : null}
          {!isHomepageLoading && !homepageError && !homepageData?.featured ? (
            <div className="empty-state">No meals are available yet.</div>
          ) : null}
        </section>
        <RestaurantResults
          query={submittedSearch?.query || ''}
          results={searchResults}
          error={searchError}
          hasSearched={hasSearched}
          onViewDetails={setSelectedMeal}
        />
        {homepageData && !homepageError ? (
          <>
            <MealSection
              title={budget ? `Meals under $${budget}` : 'Meals'}
              meals={homepageData.meals_under_budget}
              reason={budget ? `Under $${budget}` : null}
              onViewDetails={setSelectedMeal}
            />
            <MealSection
              title="Best calories per dollar"
              meals={homepageData.best_calories_per_dollar}
              reason={null}
              onViewDetails={setSelectedMeal}
            />
          </>
        ) : null}
      </main>
      {selectedMeal ? <MealDetailsDialog meal={selectedMeal} location={location} onClose={() => setSelectedMeal(null)} /> : null}
    </div>
  )
}

export default App
