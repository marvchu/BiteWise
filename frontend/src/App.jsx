import { useState } from 'react'
import './App.css'

const homepageData = {
  best_protein_per_dollar: [
    {
      id: 3,
      name: 'Double Cheeseburger',
      restaurant: 'Top Dog Grill',
      price: 6.5,
      distance: '7 min walk',
      protein_grams: 35,
      calories: 780,
      protein_per_dollar: 5.38,
      calories_per_dollar: 120,
      badge: 'Best value',
    },
    {
      id: 4,
      name: 'Grilled Chicken Sandwich',
      restaurant: 'Campus Cafe',
      price: 7.25,
      distance: '9 min walk',
      protein_grams: 38,
      calories: 520,
      protein_per_dollar: 5.24,
      calories_per_dollar: 71.72,
      badge: 'High protein',
    },
    {
      id: 1,
      name: 'Chicken Burrito Bowl',
      restaurant: 'Telegraph Taqueria',
      price: 9.5,
      distance: '11 min walk',
      protein_grams: 45,
      calories: 650,
      protein_per_dollar: 4.74,
      calories_per_dollar: 68.42,
      badge: 'Filling',
    },
  ],
  best_calories_per_dollar: [
    {
      id: 2,
      name: 'Veggie Burrito',
      restaurant: 'Telegraph Taqueria',
      price: 8,
      distance: '11 min walk',
      protein_grams: 15,
      calories: 550,
      protein_per_dollar: 1.88,
      calories_per_dollar: 68.75,
      badge: 'Under $10',
    },
    {
      id: 5,
      name: 'Bibimbap',
      restaurant: 'Bancroft Korean',
      price: 11,
      distance: '13 min walk',
      protein_grams: 28,
      calories: 600,
      protein_per_dollar: 2.55,
      calories_per_dollar: 54.55,
      badge: 'Balanced',
    },
  ],
  meals_under_price: [
    {
      id: 3,
      name: 'Double Cheeseburger',
      restaurant: 'Top Dog Grill',
      price: 6.5,
      distance: '7 min walk',
      protein_grams: 35,
      calories: 780,
      protein_per_dollar: 5.38,
      calories_per_dollar: 120,
      badge: 'Under $10',
    },
    {
      id: 4,
      name: 'Grilled Chicken Sandwich',
      restaurant: 'Campus Cafe',
      price: 7.25,
      distance: '9 min walk',
      protein_grams: 38,
      calories: 520,
      protein_per_dollar: 5.24,
      calories_per_dollar: 71.72,
      badge: 'High protein',
    },
    {
      id: 2,
      name: 'Veggie Burrito',
      restaurant: 'Telegraph Taqueria',
      price: 8,
      distance: '11 min walk',
      protein_grams: 15,
      calories: 550,
      protein_per_dollar: 1.88,
      calories_per_dollar: 68.75,
      badge: 'Under $10',
    },
  ],
}

const filters = ['High protein', 'Best value', 'Near campus']
const budgetOptions = [5, 10, 15, 20]

function formatPrice(price) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(price)
}

function Header({ isDarkMode, onToggleTheme }) {
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
        <div className="location">
          <span className="location-label">Near</span>
          <span>UC Berkeley</span>
        </div>
      </div>
    </header>
  )
}

function SearchBar({ budget, query, isSearching, onBudgetChange, onQueryChange, onSubmit }) {
  return (
    <form className="search" role="search" onSubmit={onSubmit}>
      <label htmlFor="meal-search">Find affordable meals</label>
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

function FilterChips() {
  return (
    <div className="filter-strip" aria-label="Meal filters">
      {filters.map((filter) => (
        <button className="chip" type="button" key={filter}>
          {filter}
        </button>
      ))}
    </div>
  )
}

function RestaurantResults({ query, results, error, hasSearched }) {
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
              </div>
              <strong className="result-price">
                From {formatPrice(restaurant.lowest_matching_price)}
              </strong>
              <div className="matching-items">
                {restaurant.matching_items.map((item) => (
                  <div className="matching-item" key={item.id}>
                    <span>{item.name}</span>
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

function FeaturedMeal({ meal }) {
  return (
    <section className="featured" aria-labelledby="featured-title">
      <div className="featured-copy">
        <p className="featured-label">Best option right now</p>
        <div className="featured-title-row">
          <h1 id="featured-title">{meal.name}</h1>
          <span className="featured-reason">{meal.badge}</span>
        </div>
        <p className="featured-meta">
          {meal.restaurant} - {meal.distance}
        </p>
        <div className="featured-metrics" aria-label="Featured meal metrics">
          <FeaturedMetric label="protein" value={`${meal.protein_grams}g`} />
          <FeaturedMetric label="protein per dollar" value={meal.protein_per_dollar} />
          <FeaturedMetric label="calories per dollar" value={meal.calories_per_dollar} />
        </div>
      </div>
      <div className="featured-action">
        <span className="featured-price">{formatPrice(meal.price)}</span>
        <span className="featured-price-label">total price</span>
        <button type="button">View details</button>
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

function MealCard({ meal, reason }) {
  return (
    <article className="meal-card">
      <div className="meal-card-top">
        <div className="meal-identity">
          <h3>{meal.name}</h3>
          <p>
            {meal.restaurant} - {meal.distance}
          </p>
        </div>
        <strong className="meal-price">{formatPrice(meal.price)}</strong>
      </div>
      <div className="meal-support">
        <span className="badge subtle">{reason || meal.badge}</span>
        <div className="meal-metrics">
          <MealMetric label="protein" value={meal.protein_grams ? `${meal.protein_grams}g` : null} />
          <MealMetric label="protein/$" value={meal.protein_per_dollar} />
        </div>
      </div>
      <button className="details-button" type="button">
        View details
      </button>
    </article>
  )
}

function MealSection({ title, meals, reason }) {
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
          <MealCard meal={meal} reason={reason} key={`${title}-${meal.id}`} />
        ))}
      </div>
    </section>
  )
}

function App() {
  const featuredMeal = homepageData.best_protein_per_dollar[0]
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [query, setQuery] = useState('')
  const [budget, setBudget] = useState('10')
  const [searchResults, setSearchResults] = useState([])
  const [searchError, setSearchError] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  async function handleSearch(event) {
    event.preventDefault()
    setIsSearching(true)
    setSearchError('')

    const params = new URLSearchParams()
    if (query.trim()) params.set('query', query.trim())
    if (budget) params.set('max_price', budget)

    try {
      const response = await fetch(`/api/restaurants?${params.toString()}`)
      if (!response.ok) throw new Error('Search request failed')
      setSearchResults(await response.json())
    } catch {
      setSearchResults([])
      setSearchError('Could not load restaurant results. Make sure the BiteWise API is running.')
    } finally {
      setHasSearched(true)
      setIsSearching(false)
    }
  }

  return (
    <div className="app-theme" data-theme={isDarkMode ? 'dark' : 'light'}>
      <main className="app-shell">
        <Header
          isDarkMode={isDarkMode}
          onToggleTheme={() => setIsDarkMode((current) => !current)}
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
          <FilterChips />
          <FeaturedMeal meal={featuredMeal} />
        </section>
        <RestaurantResults
          query={query.trim()}
          results={searchResults}
          error={searchError}
          hasSearched={hasSearched}
        />
        <MealSection
          title="Meals under $10"
          meals={homepageData.meals_under_price}
          reason="Under $10"
        />
        <MealSection
          title="Best protein per dollar"
          meals={homepageData.best_protein_per_dollar}
          reason="Best value"
        />
        <MealSection
          title="Best calories per dollar"
          meals={homepageData.best_calories_per_dollar}
          reason="Filling"
        />
      </main>
    </div>
  )
}

export default App
