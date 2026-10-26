# My agent: AI Personal Stylist
One-liner: A conversational stylist that turns an occasion, vibe, and budget into 2–3 curated outfits from a catalog, refines them on the fly, and lets you save or visualize your favorite look.

Core User Journey:
Describe the occasion → Get curated complete looks → Refine conversationally → Save or visualize a look

Tool coverage:
- Memory: Long-term style profile across sessions (favorite/avoided colors, general vibe/aesthetic, typical size, items/fabrics to avoid, typical budget, and saved favorite looks).
- Tools:
  - `search_catalog`: Search and filter apparel/accessories by category, occasion/vibe, season, color, and price.
  - `save_outfit`: Save a curated outfit ensemble to user favorites.
  - `get_saved_outfits`: Retrieve past saved looks.
- Catalog/UI:
  - Catalog data: A focused collection of curated apparel and accessories (tops, bottoms, outerwear, shoes, accessories) with price, occasion/vibe tags, season, and images.
  - UI/A2UI: Rich cards for complete outfits (showing item breakdowns, total price, and stylist reasoning) with side-by-side comparison tables.
- Image gen: Visual/editorial lookbook preview generating an artistic rendering of a selected complete outfit ensemble.
- Sandbox: Lightweight budget summation and validation (verifying total outfit cost remains under budget constraints).

Recommended for every project: memory (preferences & saved looks), storage/catalog, function tools (catalog search & save), image generation (editorial lookbook render), A2UI (outfit cards & tables).
Agent-specific / stretch (pick what fits): Weather tool (deriving local temperature/season automatically from city and date).
