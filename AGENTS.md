# Repository Guidelines

## Project Structure & Module Organization
This repository is a lightweight static site. `index.html` contains the UI and browser logic. `data/schwimmbaeder.js` is the source of truth for rendered entries, `data/meta.js` stores the visible last-update date, and `status_history.md` tracks later reassessments without changing the UI.

## Build, Test, and Development Commands
There is no build step or dependency install.

- `xdg-open index.html` opens the mockup directly in a browser.
- `python3 -m http.server 8000` serves the repo locally for browser testing.
- `curl -I http://127.0.0.1:8000/` checks that the local server responds.
- `uv run scripts/update_last_updated.py` refreshes `data/meta.js` with today's date.
- `uv run scripts/sync_geodata.py sync` geocodes entries with Photon and writes OSM `lat`/`lon` plus `karte`.
- `uv run scripts/sync_geodata.py check` fails if any entry is missing OSM geodata.
- `uv run scripts/check_history.py` fails if an existing bath is materially re-evaluated without updating `status_history.md`.

Prefer the local server when verifying changes to filtering, layout, or link behavior.

## Coding Style & Naming Conventions
Use 2-space indentation in HTML and inline JavaScript. Keep data objects consistent: `id`, `name`, `adresse`, `bundesland`, `region`, `status`, `begruendung`, `zeitraum`, `quelle`, `lat`, `lon`, `karte`. Use lowercase status values such as `geschlossen` and `gefaehrdet`. Assign the next highest numeric `id`; the UI shows higher IDs first within each status. Prefer normal postal addresses in the form `Straße Hausnummer, PLZ Ort` whenever a reliable source or map result supports it.

## Must-Do Data Workflow
When adding or editing an entry:

1. Update `data/schwimmbaeder.js`.
2. Run `uv run scripts/update_last_updated.py`.
3. Run `uv run scripts/sync_geodata.py sync`.
4. Run `uv run scripts/sync_geodata.py check`.
5. Mirror the content change in `schwimmbaeder.md` when it affects the published table.
6. Verify the address link opens the expected OSM location in the browser.
7. If a bath is reclassified, retained despite partial relief, or otherwise re-evaluated, append the decision and source to `status_history.md`.

Local enforcement exists through `.githooks/pre-commit`. Enable it once with `git config core.hooksPath .githooks`.
It updates `data/meta.js`, validates geodata, and requires `status_history.md` for relevant reassessments.

## Testing Guidelines
There is no full automated UI test suite yet. Validate changes manually:

- Confirm filters, counts, and search results update correctly.
- Check that new data entries render without broken layout or missing fields.
- Open a sample of source URLs and OSM links to catch malformed links.

For content edits, also verify Markdown tables in `schwimmbaeder.md`.

## Commit & Pull Request Guidelines
Use short, imperative commit subjects such as `Add Stadtroda entry` or `Switch maps to OSM`. PRs should summarize the content or UI change, list affected files, and include screenshots for visible `index.html` updates. Link the source material used for each new data point.

## Data & Source Integrity
Prefer municipal pages, operator sites, and credible local reporting. Do not add unsourced claims. If an address is incomplete, keep the wording explicit and still run geodata sync so every entry has OSM coordinates. For near-misses or temporary relief, prefer documenting the development in `status_history.md` over silently deleting or downgrading the entry.

## Needs To Be Added Back
- Re-add the `Korrektur oder Ergänzung? Wir freuen uns über Hinweise mit Quellenangabe.` callout.
- Re-add the `Impressum` footer link where it was removed from the public pages.
