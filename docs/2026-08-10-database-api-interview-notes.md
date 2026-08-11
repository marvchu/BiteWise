# 2026-08-10 Database and API Interview Notes

This document summarizes today's BiteWise backend work for resume review, project walkthroughs, and technical interview discussion.

## One-minute summary

Today we moved BiteWise from a stub-data backend toward a real database-backed API.

The project now has:

- SQLAlchemy models for restaurants, locations, and menu items
- Alembic migration setup for the first database schema
- A development seed script with real Berkeley restaurant names and approximate local data
- API services that read from the database instead of `stub_data.py`
- Tests that use an in-memory SQLite database so the DB-backed service path is covered without needing local Postgres during test runs

The important architectural shift is:

```text
Before:
router -> service -> stub_data.py

Now:
router -> service -> SQLAlchemy database session
```

## Decisions made

### 1. Start with only restaurants, locations, and menu items

We chose the first database schema to contain:

```text
restaurants
locations
menu_items
```

We intentionally deferred:

- deals
- free-food events
- price history
- location-specific menus
- automated ingestion/scrapers

Why this was the right tradeoff:

- The MVP first needs a reliable restaurant/menu foundation.
- Deals and free-food events need freshness, expiration, and verification rules.
- A smaller schema is easier to understand, seed, test, and explain.
- Adding ingestion before the schema is stable would create rework.

Strong interview framing:

> I intentionally started with the smallest schema that supports the current user flow. The goal was to avoid prematurely designing deals, free-food events, and scraping before the core restaurant/menu model was proven.

### 2. Use separate locations table

We chose:

```text
Restaurant has many Locations
Location belongs to Restaurant
```

Why:

- Some restaurants may eventually have multiple locations.
- Address and coordinates are location data, not restaurant identity data.
- It keeps the schema flexible without much added complexity.

Tradeoff:

- It adds one extra table now.
- For many Berkeley restaurants there may only be one location, so the structure is slightly ahead of current needs.

Strong interview framing:

> I separated restaurant identity from physical location. That lets the app support multi-location restaurants later without changing the restaurant model.

### 3. Attach menu items to restaurants, not locations

We chose:

```text
Restaurant has many MenuItems
MenuItem belongs to Restaurant
```

Why:

- For the MVP, one shared menu per restaurant is good enough.
- Location-specific prices/menus would complicate the schema before we know we need them.

Tradeoff:

- If two locations of the same restaurant have different prices, the model will need to evolve.

Strong interview framing:

> I kept menu items restaurant-level for the MVP because the product does not yet need branch-specific pricing. I documented that as a future limitation rather than overbuilding the first schema.

### 4. Use current price only

We chose:

```text
menu_items.price
```

and deferred:

```text
price_history
```

Why:

- Current price is enough for search, sorting, and homepage recommendations.
- Price history is useful later, but not needed to prove the first product loop.

Tradeoff:

- The app cannot yet answer "how has this price changed over time?"

Strong interview framing:

> I chose current price only because the MVP is about finding affordable options now. Price history is a later analytics feature.

### 5. Services talk directly to SQLAlchemy for now

We discussed whether to add repositories.

Options:

```text
router -> service -> repository -> database
router -> service -> database
```

We chose:

```text
router -> service -> database
```

Why:

- The app is still small.
- It is easier to learn and trace.
- The service layer already owns filtering, sorting, grouping, and metric computation.
- Adding repositories now would add ceremony before the query logic is complex enough to justify it.

Tradeoff:

- Services now contain both business logic and SQLAlchemy query code.
- If queries are reused across ingestion/admin flows later, a repository layer may become useful.

Strong interview framing:

> I considered a repository layer but chose to keep services talking directly to SQLAlchemy for the MVP. It keeps the code easier to follow, and I can extract repositories later if query logic becomes reused or complex.

## What was implemented

### Database configuration

Added:

```text
backend/app/core/config.py
backend/app/db/base.py
backend/app/db/session.py
```

Purpose:

- `config.py` reads `DATABASE_URL`
- `base.py` defines the shared SQLAlchemy `Base`
- `session.py` creates the SQLAlchemy engine/session and exposes `get_db`

Interview point:

> `get_db` is the FastAPI dependency that gives each request a database session and closes it afterward.

### SQLAlchemy models

Added:

```text
backend/app/models/restaurant.py
backend/app/models/location.py
backend/app/models/menu_item.py
```

Model relationships:

```text
Restaurant.locations
Restaurant.menu_items
Location.restaurant
MenuItem.restaurant
```

Important modeling choices:

- `MenuItem.price` is numeric with two decimals.
- `protein_grams` and `calories` are nullable.
- `category` supports conservative search and future image fallback.
- `source_url` supports data provenance.

Interview point:

> Missing nutrition is modeled as nullable because unknown nutrition is not the same as zero nutrition.

### Alembic migration setup

Added:

```text
backend/alembic.ini
backend/alembic/env.py
backend/alembic/script.py.mako
backend/alembic/versions/20260810_0001_create_restaurant_location_menu_item_tables.py
```

Purpose:

- `alembic.ini` configures Alembic.
- `env.py` connects Alembic to the app's SQLAlchemy metadata.
- the migration file creates the first three tables.

Tables created:

```text
restaurants
locations
menu_items
```

Indexes added for likely query fields:

- restaurant name
- location restaurant id
- menu item restaurant id
- menu item name
- menu item category
- menu item price

Interview point:

> Alembic lets the database schema evolve in versioned, reviewable steps instead of relying on manual table creation.

### Development seed script

Added:

```text
backend/scripts/seed_dev_data.py
```

It seeds:

- 5 real Berkeley-area restaurant names
- 1 location per restaurant
- 2 menu items per restaurant
- approximate prices, nutrition, and coordinates

Important caveat:

The seed data is development data only. It is intentionally marked as approximate and unverified.

Why this matters:

- It gives realistic local data for development.
- It avoids pretending we have verified production data.
- It lets search, price filtering, and nullable nutrition behavior be tested.

Interview point:

> I used real restaurant names with approximate development data, but explicitly documented that the seed data is not production truth.

### API services switched from stub data to database

Changed:

```text
backend/app/services/menu_items.py
backend/app/services/restaurants.py
```

Before:

```text
services imported db.stub_data
```

Now:

```text
services accept a SQLAlchemy Session
services query SQLAlchemy models directly
services return the same Pydantic response schemas
```

Menu item service now:

- queries `MenuItem` model
- applies price/nutrition filters in SQLAlchemy
- converts models to Pydantic schemas
- computes protein/calorie value metrics
- sorts by price or computed metrics

Restaurant service now:

- queries `Restaurant` model
- uses menu item service for eligible menu items
- groups matching items by restaurant
- uses the first location's address as the response address for now

Interview point:

> I preserved the API response contracts while changing the data source underneath from stub data to SQLAlchemy.

### Routers now inject database sessions

Changed:

```text
backend/app/routers/menu_items.py
backend/app/routers/restaurants.py
backend/app/routers/homepage.py
```

Routers now use:

```python
db: Session = Depends(get_db)
```

Why:

- routers still handle HTTP concerns
- services receive the database session and handle backend logic
- FastAPI manages session lifecycle through dependency injection

Interview point:

> The routers stay thin: they validate request parameters, pass the session to services, and translate missing resources into HTTP errors.

### Tests moved to database-backed behavior

Changed:

```text
backend/tests/conftest.py
backend/tests/test_menu_items_service.py
```

Added earlier:

```text
backend/tests/test_db_models.py
backend/tests/test_seed_dev_data.py
```

Test strategy:

- use in-memory SQLite for tests
- create SQLAlchemy tables from metadata
- seed test data before each test session use
- override FastAPI's `get_db` dependency

Why:

- tests prove services and APIs work through SQLAlchemy
- tests do not require local Postgres
- existing API expectations remain stable

Validation result:

```text
29 passed, 1 warning
```

The warning is a FastAPI/Starlette `TestClient` dependency warning, not a failing test.

Interview point:

> I used SQLite for tests so the DB-backed code path is covered quickly without requiring a running Postgres instance in every test environment.

## Important technical walkthrough

### Menu item API request

Example:

```text
GET /menu-items?max_price=8&min_protein=30&sort=price
```

Flow:

```text
menu_items router
  -> FastAPI validates query params
  -> get_db provides SQLAlchemy Session
  -> menu_items service builds SQLAlchemy query
  -> filters price and protein in the database query
  -> converts DB models to Pydantic schemas
  -> computes value metrics
  -> sorts results
  -> router returns response model
```

### Restaurant search request

Example:

```text
GET /restaurants?query=burrito&max_price=10
```

Flow:

```text
restaurants router
  -> get_db provides Session
  -> restaurants service gets eligible menu items from menu_items service
  -> service matches query against item name/category
  -> service groups matching items under restaurants
  -> service sorts restaurants by lowest matching price
  -> API returns RestaurantSearchResult list
```

### Homepage request

Example:

```text
GET /homepage?max_price=10
```

Flow:

```text
homepage router
  -> get_db provides Session
  -> menu_items service returns meals under budget
  -> cheapest qualifying item becomes featured
  -> nutrition sections are built from DB-backed menu item queries
  -> active_deals and free_food_today remain empty placeholders
```

## Tradeoffs and honest limitations

### Services now mix business logic and SQLAlchemy

This was chosen deliberately for MVP simplicity.

Risk:

- service files can grow crowded if query complexity increases

Future response:

- extract repositories later if queries are reused by ingestion, admin tools, or multiple services

### SQLite tests are not identical to Postgres

SQLite is useful for fast tests, but Postgres-specific behavior may differ.

Risk:

- numeric precision, constraints, or SQL dialect behavior can differ

Future response:

- add at least one integration test path against local/test Postgres before production

### API now needs a real database in normal dev mode

Tests work with SQLite overrides, but running the app normally requires:

```text
DATABASE_URL
python -m alembic upgrade head
python scripts/seed_dev_data.py
```

Risk:

- developers need database setup before using endpoints locally

Future response:

- document setup clearly and maybe add a one-command dev setup script

### `stub_data.py` still exists

The services no longer use it, but the file remains.

Reason:

- it can be used temporarily as reference while validating the database switch

Future response:

- delete it once the database-backed flow is fully confirmed locally

### Seed data is approximate

The seed script uses real Berkeley restaurant names, but sample prices/nutrition/coordinates are approximate.

Risk:

- should not be presented as verified restaurant data

Future response:

- replace with verified manual data and source URLs before public demo

## Strong resume framing

Good bullet:

> Migrated a FastAPI MVP from in-memory stub data to SQLAlchemy-backed services with Alembic migrations, request-scoped DB sessions, SQLite-backed API tests, and repeatable development seed data.

More detailed bullet:

> Designed and implemented the first BiteWise database layer with Restaurant, Location, and MenuItem models, versioned Alembic migrations, nullable nutrition fields, source metadata, and DB-backed service logic for menu filtering, homepage recommendations, and restaurant search.

Testing-focused bullet:

> Added database-backed test coverage using FastAPI dependency overrides and in-memory SQLite to validate API behavior without requiring a local Postgres instance.

## Questions interviewers might ask

### Why did you not use repositories?

Answer:

> For this MVP, I kept SQLAlchemy access inside the service layer because the app is small and easier to learn that way. Routers remain thin, and services own the backend logic. If query logic becomes reused by ingestion/admin flows or starts crowding the services, I would extract repositories.

### Why SQLite for tests if production is Postgres?

Answer:

> SQLite makes tests fast and independent of local infrastructure. It validates the service/API path through SQLAlchemy. I would still add Postgres integration tests before production because dialect behavior can differ.

### Why keep nutrition nullable?

Answer:

> Missing nutrition is common for independent restaurants. Null preserves the truth that data is unknown. Treating missing values as zero would corrupt rankings and filters.

### Why source_url?

Answer:

> Source URL is data provenance. It lets us answer where a restaurant, menu item, price, or nutrition value came from and supports future verification workflows.

### Why current price only?

Answer:

> Current price supports the MVP user question: what can I afford now? Price history is useful later, but it would add complexity before the core search and recommendation flow is proven.

### Why still keep stub_data.py?

Answer:

> It is no longer used by services. I kept it temporarily as reference during the migration. Once the DB-backed flow is confirmed locally, it can be deleted.

## What to do next

1. Run Alembic against a real local Postgres database.
2. Run the dev seed script against that database.
3. Start FastAPI and manually verify `/menu-items`, `/restaurants`, and `/homepage`.
4. Remove or archive `stub_data.py`.
5. Add setup documentation for local Postgres.
6. Connect the frontend homepage sections to `GET /homepage`.
7. Add Postgres-backed integration checks once the local database setup is stable.

