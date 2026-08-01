Act as a senior product designer and frontend engineer reviewing the current BiteWise homepage.

First inspect the existing frontend code and the attached screenshots. Do not immediately rewrite the page.

BiteWise helps Berkeley students quickly answer:

“What is the best affordable meal near me right now?”

The current layout is functional, but it still looks generic and AI-generated. The goal is to make it feel intentional, polished, highly scannable, and suitable for a real consumer product.

Use these products only as design inspiration:

- Uber: clear next action and simple interaction flow
- Google Flights: easy comparison, sorting, and filtering
- MacroFactor: restrained color, strong typography, clean data presentation, spacing, and alignment

Do not copy their branding, assets, or exact layouts.

Before editing, identify:

1. Why the current page feels generic
2. Which elements currently have the same visual weight
3. Where borders are being overused
4. Where information hierarchy is weak
5. Which components should be reused or changed
6. Which files you plan to modify

Then redesign the homepage according to these requirements.

DESIGN PRINCIPLES

1. Create clear visual hierarchy

The user should immediately notice, in this order:

- The search and filter controls
- The best recommendation right now
- The meal result sections
- Supporting nutrition metrics

The primary recommendation must feel meaningfully more important than ordinary meal cards.

2. Use layered surfaces

Do not place every element inside an identical white bordered rectangle.

Create subtle visual layers using:

- An off-white or lightly tinted page background
- A distinct search or hero region
- A clearly differentiated featured recommendation
- White content surfaces where needed
- Spacing and dividers instead of borders everywhere

3. Reduce border dependence

Avoid giving every chip, card, section, and control a visible outline.

Prefer:

- Whitespace
- Section spacing
- Subtle background changes
- Thin dividers
- Typography hierarchy

Use borders only when they clarify grouping or interaction.

4. Make the featured meal genuinely featured

The “Best option right now” section should be the strongest focal point after search.

It should include:

- Recommendation label
- Meal name
- Restaurant name
- Price
- Walking time or distance
- Two or three useful metrics
- A clear view-details action

Use a distinct layout, stronger typography, and restrained accent treatment. Do not make it look like a larger version of the ordinary cards.

5. Redesign ordinary meal cards

The current cards feel too much like tables.

Make them easier to scan in roughly one second.

Prioritize:

1. Meal name
2. Price
3. Restaurant
4. Walking time
5. One recommendation badge
6. One or two important nutrition/value metrics
7. View-details action

Do not give every metric equal emphasis.

Avoid rigid spreadsheet-like metric grids unless they clearly improve comparison.

Do not display missing nutrition values as zero.

6. Use color with restraint

Do not solve the problem by adding many colors.

Use a limited palette:

- Warm white or neutral page background
- Dark near-black text
- Muted secondary text
- One primary BiteWise green
- A lighter green tint for badges or selected filters
- At most one optional warm accent for special states such as “Hot deal” or “Free today”

Create hierarchy using shade, weight, and spacing rather than saturation.

7. Improve typography

Use a deliberate type scale.

Suggested hierarchy:

- Page or hero heading: strongest
- Featured meal title: large and prominent
- Section heading: clear but smaller
- Meal card title: medium emphasis
- Price: bold and easy to compare
- Supporting labels: small and muted
- Nutrition metrics: compact but readable

Avoid excessive uppercase text. Reserve uppercase for very small labels only.

8. Improve alignment and spacing

Use consistent spacing tokens rather than arbitrary values.

Ensure:

- Search controls align cleanly
- Filter chips share height and padding
- Prices align consistently across result cards
- Card content follows a repeatable vertical rhythm
- Section gaps are larger than gaps within components
- Mobile touch targets are comfortable

9. Consider food imagery carefully

Food is an emotional product, but imagery should not dominate the MVP.

If existing data does not include reliable food images:

- Do not use random stock photos
- Do not add emoji as a substitute throughout the interface
- Create cards that still look complete without imagery
- Leave a clean optional image slot only if the component supports both states well

Future imagery approach:

- Prefer explicit `image_url` or `image_asset_key` data on a menu item when a real, verified image exists.
- If a menu item does not have its own image, do not guess a specific photo from the item name.
- Use a simple food category only as a fallback, such as `bowl`, `burger`, `sandwich`, `burrito`, `noodles`, `rice`, `salad`, `drink`, or `unknown`.
- Category fallback imagery should be generic and intentionally abstract, not a photo pretending to be the exact meal.
- The UI should support three states: verified item image, category fallback visual, and no image.
- Do not let imagery displace the core comparison information: meal name, price, restaurant, walking time, recommendation reason, and key metrics.

Possible classification rules for later:

- Store `category` manually in seed data first. This is easiest to review and avoids bad automatic guesses.
- Later, infer a category from normalized item names using conservative keyword matching.
- When keyword matching is uncertain, use `unknown` and render the no-image card state.
- Never infer ratings, popularity, taste, portion size, or quality from an image category.

10. Preserve product clarity

Do not add:

- Large decorative illustrations
- Glassmorphism
- Heavy shadows
- Strong gradients
- Excessive animation
- Multiple competing accent colors
- Fake ratings or data not provided by the API
- New product features
- A large marketing landing-page hero

This should still feel like a utility that helps users make a fast food decision.

TECHNICAL REQUIREMENTS

- Preserve the current frontend framework and styling approach
- Reuse existing components where practical
- Break large components into focused reusable components
- Keep presentational components separate from data fetching
- Do not modify the backend
- Do not change the API response shape
- Preserve loading, error, and empty states
- Use semantic HTML
- Maintain keyboard accessibility and visible focus states
- Support mobile and desktop layouts
- Avoid unnecessary dependencies
- Do not rewrite unrelated files

IMPLEMENTATION PROCESS

1. Explain the proposed design changes briefly
2. List the files you will change
3. Implement the redesign
4. Run the formatter
5. Run the linter
6. Run the type checker
7. Run relevant tests
8. Summarize what changed and identify any assumptions

When choosing between a more decorative design and a simpler design, choose the simpler design.
