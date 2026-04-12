# Repository Guidelines

## Project Structure & Module Organization
This repository is a lightweight static site. `index.html` contains the UI and browser logic. `data/schwimmbaeder.js` is the source of truth for rendered entries. `schwimmbaeder.md` is the public research table, and `scripts/sync_geodata.py` maintains OSM coordinates and map links.

## Build, Test, and Development Commands
There is no build step or dependency install.

- `xdg-open index.html` opens the mockup directly in a browser.
- `python3 -m http.server 8000` serves the repo locally for browser testing.
- `curl -I http://127.0.0.1:8000/` checks that the local server responds.
- `uv run scripts/sync_geodata.py sync` geocodes entries with Photon and writes OSM `lat`/`lon` plus `karte`.
- `uv run scripts/sync_geodata.py check` fails if any entry is missing OSM geodata.

Prefer the local server when verifying changes to filtering, layout, or link behavior.

## Coding Style & Naming Conventions
Use 2-space indentation in HTML and inline JavaScript. Keep data objects consistent: `id`, `name`, `adresse`, `bundesland`, `region`, `status`, `begruendung`, `zeitraum`, `quelle`, `lat`, `lon`, `karte`. Use lowercase status values such as `geschlossen` and `gefaehrdet`. Assign the next highest numeric `id`; the UI shows higher IDs first within each status.

## Must-Do Data Workflow
When adding or editing an entry:

1. Update `data/schwimmbaeder.js`.
2. Run `uv run scripts/sync_geodata.py sync`.
3. Run `uv run scripts/sync_geodata.py check`.
4. Mirror the content change in `schwimmbaeder.md` when it affects the published table.
5. Verify the address link opens the expected OSM location in the browser.

Local enforcement exists through `.githooks/pre-commit`. Enable it once with `git config core.hooksPath .githooks`.

## Testing Guidelines
There is no full automated UI test suite yet. Validate changes manually:

- Confirm filters, counts, and search results update correctly.
- Check that new data entries render without broken layout or missing fields.
- Open a sample of source URLs and OSM links to catch malformed links.

For content edits, also verify Markdown tables in `schwimmbaeder.md`.

## Commit & Pull Request Guidelines
Use short, imperative commit subjects such as `Add Stadtroda entry` or `Switch maps to OSM`. PRs should summarize the content or UI change, list affected files, and include screenshots for visible `index.html` updates. Link the source material used for each new data point.

## Data & Source Integrity
Prefer municipal pages, operator sites, and credible local reporting. Do not add unsourced claims. If an address is incomplete, keep the wording explicit and still run geodata sync so every entry has OSM coordinates.
