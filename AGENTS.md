# BiteWise Development Instructions

## Product purpose

BiteWise helps Berkeley students quickly answer:

"What is the best affordable food option near me right now?"

The application should prioritize fast decision-making. Users should be able to understand the best options within a few seconds without reading large amounts of text.

## Frontend design direction

The BiteWise UI should combine:

- Uber's action-focused simplicity
- Google Flights' comparison and filtering experience
- MacroFactor's clean, polished, data-oriented visual style

Use these products only as design inspiration. Do not directly copy their layouts, branding, assets, or proprietary visual elements.

## Overall visual style

Build a modern, minimal interface with:

- A clean white or very light neutral background
- Dark, high-contrast typography
- One restrained BiteWise accent color
- Generous spacing
- Clear visual hierarchy
- Rounded corners used consistently
- Thin borders rather than heavy shadows
- Smooth but subtle hover and transition states
- A polished mobile/web hybrid layout
- Strong readability and accessible contrast

Avoid:

- Excessive gradients
- Glassmorphism
- Large decorative illustrations
- Heavy drop shadows
- Too many accent colors
- Dense dashboards
- Tiny text
- Excessive animations
- Generic AI-generated landing-page styling
- Making every section look like a floating card

## Design principles

### 1. Action-focused like Uber

The primary action should always be obvious.

On the homepage, emphasize:

- Location
- Search
- Budget
- Recommended meals

Do not make users navigate through multiple screens before seeing useful food options.

### 2. Comparable like Google Flights

Users should be able to quickly compare options by:

- Price
- Distance
- Protein
- Calories
- Protein per dollar
- Calories per dollar

Use compact filter chips and sorting controls instead of large filter forms.

Clearly explain why an item is recommended using labels such as:

- Best value
- High protein
- Under $10
- Closest
- Free today

### 3. Polished and data-oriented like MacroFactor

Present numerical information clearly without making the interface feel like a spreadsheet.

Use:

- Large prominent values for price
- Smaller muted labels for supporting metrics
- Consistent metric formatting
- Clean dividers
- Compact data rows
- Strong spacing between information groups
- Simple icons only where they improve comprehension

Food imagery and emoji should be used sparingly. The interface should still look polished when an item has no image.

## Information hierarchy

For each meal, prioritize information in this order:

1. Meal name
2. Price
3. Restaurant
4. Distance or walking time
5. Recommendation reason
6. Nutrition and value metrics
7. Secondary action

Do not give every piece of information equal visual weight.

## Meal card requirements

Each meal card should include:

- Meal name
- Restaurant name
- Price
- Distance or walking time when available
- One primary recommendation badge
- Relevant nutrition metrics when available
- A clear action to view details

Do not display missing nutrition values as zero.

Do not overload cards with every available backend field.

Cards should be easy to scan vertically on mobile and easy to compare in a row or grid on desktop.

## Homepage structure

The initial homepage should contain:

1. Header with BiteWise branding and location
2. Search input
3. Compact filter chips
4. A highlighted best recommendation
5. Meals under the selected budget
6. Best protein per dollar
7. Free food today, when data exists

Do not add unnecessary sections merely to fill the page.

## Responsive behavior

Design mobile-first.

Mobile:
- Single-column results
- Horizontally scrollable filter chips
- Comfortable touch targets
- Important actions reachable without precise tapping
- Avoid horizontal page overflow

Desktop:
- Centered content with a reasonable maximum width
- More room for comparison
- Two- or three-column card layouts where appropriate
- Do not stretch content across the entire screen

## Accessibility

- Use semantic HTML
- Associate labels with controls
- Ensure keyboard navigation works
- Include visible focus states
- Use accessible color contrast
- Do not communicate meaning using color alone
- Add descriptive accessible names to icon-only buttons
- Respect reduced-motion preferences

## React architecture

Prefer small reusable components such as:

- Header
- LocationSelector
- SearchBar
- FilterChips
- MealCard
- FeaturedMeal
- MealSection
- EmptyState
- LoadingSkeleton

Keep data fetching separate from presentational components.

Do not place the entire homepage in one large component.

Avoid unnecessary state. Derive values from existing state when possible.

## Implementation workflow

Before making major UI changes:

1. Inspect the existing frontend structure.
2. Reuse existing components and tokens when appropriate.
3. Briefly describe the proposed component structure.
4. Implement one page or feature at a time.
5. Run the available formatter, linter, type checker, and tests.
6. Report what changed and any remaining issues.

Do not rewrite unrelated files.

When visual requirements are ambiguous, choose the simpler interface.