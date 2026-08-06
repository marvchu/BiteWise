# BiteWise Project Discussion Prep

Use this document to prepare for resume reviews, project walkthroughs, and interview questions. It focuses on what was actually built, why the decisions were made, and how to explain the tradeoffs honestly.

## One-minute explanation

BiteWise is a Berkeley student food-savings app that helps answer:

> What is the best affordable food option near me right now?

The product is price-first. Nutrition metrics like protein per dollar and calories per dollar are useful enrichment, but they are optional because many independent restaurants do not publish reliable nutrition data. The app should still help a student find affordable food even when nutrition is unknown.

Current stack:

- Frontend: React with Vite
- Backend: FastAPI with Pydantic schemas
- Data: in-memory stub data for now
- Future persistence: PostgreSQL, SQLAlchemy, Alembic

## Product direction

The project started with menu items and value metrics. The key product refinement was that BiteWise should not become only a nutrition optimizer. The strongest use case is affordability and fast comparison.

Good framing:

- Students care first about price, nearby options, and deals.
- Nutrition is useful when available, but should not exclude restaurants.
- Search should help answer which restaurants have a requested food within budget.
- The homepage should immediately show useful options without making users navigate first.

## Architecture decisions

### 1. Keep routers, services, schemas, and data separate

Current backend shape:

```text
Router -> Service -> Stub data -> Schema
```

Routers handle HTTP behavior:

- query parameters
- route paths
- response models
- HTTP errors

Services handle application logic:

- filtering
- sorting
- metric calculation
- grouping search results

Schemas define contracts:

- what fields responses contain
- which fields are nullable
- how nested data is shaped

Stub data temporarily replaces a real database:

- easier to move quickly
- avoids locking in a database schema too early
- keeps the service/router contracts testable

Tradeoff: this is more structure than putting everything in route functions, but it makes the app easier to grow and test.

### 2. Rename service list behavior for clarity

The menu-items service function was renamed from `get_menu_items` to `list_menu_items`.

Reason:

- `get_menu_item(id)` means "fetch one item"
- `list_menu_items(...)` means "fetch many items, optionally filtered/sorted"

This makes the code easier to explain and reduces confusion between router functions and service functions.

Tradeoff: renaming required updating routers and tests, but improved readability.

### 3. Move homepage response schema out of the router

`HomepageResponse` was moved into `schemas/homepage.py`.

Reason:

- routers should define API paths
- schemas should define response shapes
- moving the schema makes the architecture easier to teach and maintain

Tradeoff: one extra file/import, but cleaner ownership.

### 4. Keep nutrition nullable

Nutrition fields remain optional:

- `protein_grams`
- `calories`
- `protein_per_dollar`
- `calories_per_dollar`

Rules:

- missing nutrition is not displayed as zero
- derived metrics become `None` when data is missing
- sorting places missing metric values last
- nutrition filters exclude records missing the requested nutrition field

Tradeoff: frontend and tests need to handle nulls, but the data is honest.

### 5. Make homepage price-first

The backend homepage contract now supports:

```text
featured
meals_under_budget
active_deals
free_food_today
best_protein_per_dollar
best_calories_per_dollar
```

`GET /homepage?max_price=10` uses a configurable budget.

Reason:

- price and budget are the core product behavior
- deals and free-food sections are future-facing but explicit
- nutrition sections stay available without controlling the whole product

Tradeoff: `active_deals` and `free_food_today` currently return empty lists, so the contract is ahead of the data model.

### 6. Add restaurant-level search

The app now supports:

```text
GET /restaurants?query=burrito&max_price=10
GET /restaurants/{restaurant_id}
```

Search returns restaurants with matching menu items and a lowest matching price.

Reason:

- users often think "where can I get a burrito under $10?"
- grouping by restaurant matches the real decision better than a flat list of items
- backend grouping prevents duplicated ranking logic in React

Tradeoff: the restaurant-search response is more product-specific, but the flat `GET /menu-items` endpoint still exists for meal-level browsing.

### 7. Use conservative search first

Restaurant search uses case-insensitive substring matching against:

- menu item name
- manually assigned category

Reason:

- simple
- predictable
- easy to test
- appropriate for a small seeded MVP

Tradeoff: it does not handle synonyms, typos, semantic meaning, or advanced ranking.

### 8. Use Vite proxy for local API calls

The frontend calls:

```text
/api/restaurants
```

Vite proxies it to:

```text
http://127.0.0.1:8000/restaurants
```

Reason:

- keeps frontend fetch URLs clean
- avoids local CORS setup during development

Tradeoff: production still needs environment-aware API configuration.

## Frontend design decisions

### 1. Build a real app screen, not a landing page

The Vite starter screen was replaced with a BiteWise homepage.

Current homepage includes:

- header with brand, location, and dark-mode toggle
- search input
- budget selector
- filter chips
- featured recommendation
- restaurant search results
- reusable meal sections
- reusable meal cards
- loading, empty, and error states for search

Reason:

- BiteWise is a utility product
- the first screen should help users make a food decision
- a marketing-style hero would not match the product goal

### 2. Use reusable components

Main React components:

- `Header`
- `SearchBar`
- `FilterChips`
- `RestaurantResults`
- `FeaturedMeal`
- `FeaturedMetric`
- `MealCard`
- `MealMetric`
- `MealSection`

Reason:

- easier to understand
- easier to test later
- avoids one giant homepage component

Tradeoff: more component functions in one file for now. Later, these can move into separate component files.

### 3. Keep data fetching separate from presentation where practical

Search state and fetch behavior live in `App`.

Presentational components receive props:

- `SearchBar` receives query, budget, loading state, and callbacks
- `RestaurantResults` receives results, errors, and search state
- `MealCard` receives one meal

Reason:

- components stay easier to reason about
- future API integration can be improved without rewriting every card

Tradeoff: `App.jsx` is now fairly large and should eventually be split.

### 4. Make the UI less template-like

Several visual passes were made:

- reduced repeated identical card boxes
- removed generic section subtitles
- reduced excessive pills
- demoted ordinary "View details" actions
- made the featured recommendation visually stronger
- limited visible metrics on ordinary cards
- consolidated color, spacing, radius, and shadow tokens

Reason:

- avoid a generic dashboard feel
- emphasize real user decision hierarchy
- make the page scannable in seconds

Tradeoff: less explanatory text on screen means the UI relies more on clear structure.

### 5. Add dark mode with full-page theme scope

Dark mode was added with React state and `data-theme`.

Important correction:

- first version scoped dark mode to `.app-shell`, so only the centered content changed
- it was fixed by adding `.app-theme` as a full-page wrapper

Reason:

- the whole viewport should participate in theme changes
- dark mode should not look like a dark card floating on a light page

Tradeoff: current dark mode is local state only. It does not persist to local storage or follow system preference yet.

### 6. Document imagery instead of faking it

Imagery was not implemented yet.

Instead, docs were updated with future guidance:

- prefer verified item images
- support category fallback visuals
- support a no-image state
- do not use random stock photos
- do not guess exact food images from item names

Reason:

- bad imagery would make the app look less trustworthy
- current data does not include image fields

Tradeoff: the UI is less emotional without food images, but more honest.

## What was actually implemented

### Backend

- Added unit/API tests for menu item services and API routes.
- Added restaurant API routes.
- Added restaurant schemas.
- Added restaurant service logic for grouping matching items by restaurant.
- Registered the restaurant router in `main.py`.
- Added homepage schema in `schemas/homepage.py`.
- Changed homepage response to a price-first contract with `featured`, `meals_under_budget`, deals, free-food, and nutrition sections.
- Added deal/free-food summary schemas as placeholders.
- Added calorie filters in the menu item service.
- Kept nutrition nullable and metrics computed only when possible.
- Renamed `get_menu_items` to `list_menu_items`.
- Renamed the single-item router handler to `read_menu_item`.
- Added/updated tests for menu item behavior, homepage behavior, and restaurant behavior.

### Frontend

- Replaced the Vite starter screen with the BiteWise homepage.
- Added reusable React components for header, search, filters, featured meal, meal cards, meal sections, and restaurant results.
- Added search form state.
- Added budget selector state.
- Connected restaurant search to `/api/restaurants`.
- Added loading, empty, and error states for restaurant search.
- Added Vite proxy from `/api` to FastAPI.
- Added responsive styling for mobile and desktop.
- Added a dark mode toggle.
- Fixed dark mode to cover the full viewport.
- Refined card hierarchy, featured section hierarchy, surfaces, colors, badges, buttons, and tokens.

### Documentation

- Read and followed `AGENTS.md`.
- Extended `docs/frontend.md` with imagery rules and future classification strategy.
- Extended `docs/data` with future image/category fields.
- Added this project discussion prep doc.

## Validation performed

Frontend:

```text
npm.cmd run lint
npm.cmd run build
```

Both passed after the frontend changes.

Backend:

Earlier menu item and API tests passed after initial test setup:

```text
17 passed
```

The repo now also contains restaurant tests. Before claiming all backend tests pass in a resume or interview, run:

```text
cd backend
python -m pytest
```

Be honest if the local environment changes or tests fail.

## Current limitations

- The homepage meal sections still use static frontend sample data.
- Restaurant search is connected to the backend, but the featured homepage cards are not fully API-driven.
- Filter chips like "High protein" and "Near campus" are visual only.
- View-details buttons do not navigate yet.
- There is no persistent database.
- There are no Alembic migrations yet.
- Deals and free-food events are placeholders, not complete features.
- Distance/walking time is static and not computed.
- Dark mode does not persist across refresh.
- Search is simple substring/category matching.
- No frontend automated tests have been added yet.
- Food imagery is documented but not implemented.

## Strong interview framing

Use this:

> I built a React/FastAPI vertical slice for a student food-savings app, with reusable frontend components, restaurant search, price filtering, nullable nutrition metrics, Pydantic response contracts, service-layer business logic, and focused API/unit test coverage.

Also good:

> I intentionally kept the first version price-first because the user problem is affordability, not perfect nutrition tracking. Nutrition enriches the experience when available, but missing nutrition should not exclude local restaurants.

Avoid claiming:

- production deployment
- real PostgreSQL persistence
- live restaurant data
- verified nutrition accuracy
- real distance calculations
- completed maps
- implemented food imagery
- fully connected homepage data

## Likely resume grilling questions

### Why FastAPI?

FastAPI gives typed request/response validation with Pydantic, automatic Swagger docs, and a clean way to separate routers from service logic. It is lightweight enough for an MVP but structured enough to grow.

### Why React/Vite?

React fits the component-based UI, and Vite gives fast local development with a simple build setup. The Vite proxy also made local API calls easier without CORS work.

### Why not build the database first?

The product model was still changing. Stub data let the API contract, user flow, and frontend behavior be tested before locking relationships into migrations.

### Why group restaurant search on the backend?

Because the product question is restaurant-oriented: "Where can I get this food under this budget?" Grouping on the backend keeps ranking and filtering consistent across clients.

### Why are nutrition fields nullable?

Because missing nutrition is real data uncertainty. Treating missing values as zero would be wrong and would corrupt rankings. Nulls force the UI and service logic to handle uncertainty honestly.

### Why not use AI or semantic search?

The MVP dataset is small. Substring/category matching is deterministic and testable. More advanced search should come after real query data proves it is needed.

### Why add dark mode?

It was a scoped UI enhancement that exercised the design token system. The first implementation revealed an important scoping issue, which was fixed by applying the theme at the full-page wrapper level.

### Why not add food images immediately?

Food images can improve emotional appeal, but fake or mismatched images reduce trust. The app needs verified image fields or conservative category fallback before imagery belongs in the UI.

## Strong technical walkthrough

When a user searches for burritos under $10:

```text
React form submit
  -> App builds URLSearchParams
  -> fetch('/api/restaurants?query=burrito&max_price=10')
  -> Vite proxy rewrites /api to FastAPI
  -> restaurants router validates query params
  -> restaurants service gets price-eligible menu items
  -> service matches item name/category
  -> service groups matching items by restaurant
  -> service sorts restaurants by lowest matching price
  -> React renders restaurant result cards
```

When a user opens the homepage API:

```text
GET /homepage?max_price=10
  -> homepage router validates max_price
  -> menu_items service lists items under budget sorted by price
  -> first budget item becomes featured
  -> nutrition sections are populated from items with nutrition data
  -> empty deal/free-food arrays make unfinished features explicit
```

## Best next steps

1. Run the full backend test suite and fix any drift.
2. Connect the homepage sections to `GET /homepage`.
3. Move frontend components out of `App.jsx` into component files.
4. Add frontend tests for search, loading, error, and empty states.
5. Design the PostgreSQL schema with restaurants, locations, menu items, deals, and free-food events.
6. Add SQLAlchemy models and Alembic migrations.
7. Add real detail pages for restaurants and menu items.
8. Define distance/location behavior before building the map.
9. Add image/category fields only after agreeing on the data strategy.

## Best resume bullets

Use one of these depending on the role:

- Built a React/FastAPI food-savings app that groups menu-item search results by restaurant, applies budget constraints, and preserves nullable nutrition data for incomplete real-world menus.
- Designed a layered FastAPI backend with routers, services, Pydantic schemas, stub repositories, and API/unit tests for price filtering, value metrics, homepage responses, and restaurant search.
- Implemented a responsive BiteWise homepage in React with reusable meal-card components, budget search, restaurant results, loading/error/empty states, Vite API proxying, and dark-mode theming.
- Created product/design documentation covering visual hierarchy, imagery strategy, data tradeoffs, and MVP limitations.

## What to say if challenged

If asked whether this is production-ready:

> Not yet. It is an MVP vertical slice. The API and UI contracts are in place, but persistence, real data ingestion, location, maps, deals, and homepage API integration still need to be completed.

If asked what you are most proud of:

> I kept the product honest. Missing nutrition is not treated as zero, fake images were not added, and the backend groups search results around the user's real decision: which restaurant can give me this food within my budget?

If asked what you would do differently:

> I would split the frontend components into separate files sooner and add frontend tests once the first connected search flow stabilized.
