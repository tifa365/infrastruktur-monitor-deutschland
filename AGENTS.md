# Repository Guidelines

## Project Structure & Module Organization
This repository is a lightweight browser mockup, not a packaged app. `index.html` contains the full UI, inline styling via Tailwind CDN, and the in-page JavaScript dataset used to render filters, statistics, and source links. `schwimmbaeder.md` is the curated research table for pool closures and risks. `quellen.md` collects overview sources and research entry points. `README.md` explains scope, status, and licensing.

## Build, Test, and Development Commands
There is no build step or dependency install.

- `xdg-open index.html` opens the mockup directly in a browser.
- `python3 -m http.server 8000` serves the repo locally for browser testing.
- `curl -I http://127.0.0.1:8000/` is a quick check that the local server is responding.

Prefer the local server when verifying changes to filtering, layout, or link behavior.

## Coding Style & Naming Conventions
Use 2-space indentation in HTML, CSS classes, and inline JavaScript to match `index.html`. Keep markup semantic and keep JavaScript straightforward; this repo currently uses plain objects and arrays rather than modules or build tooling. Use descriptive German content fields such as `bundesland`, `begruendung`, and `zeitraum`. When adding entries, preserve the existing object shape and lowercase status values such as `geschlossen` and `gefaehrdet`.

## Testing Guidelines
There is no automated test suite yet. Validate changes manually in the browser:

- Confirm filters, counts, and search results update correctly.
- Check that new data entries render without broken layout or missing fields.
- Open a sample of source URLs and map links to catch malformed links.

For content edits, also verify Markdown tables in `schwimmbaeder.md` and link formatting in `quellen.md`.

## Commit & Pull Request Guidelines
Git history is not available in this checkout, so no repository-specific commit pattern could be derived here. Use short, imperative commit subjects such as `Add new pool closure entry` or `Refine filter rendering`. PRs should summarize the content or UI change, list affected files, and include screenshots for visible `index.html` updates. Link the source material or issue used for each new data point.

## Data & Source Integrity
This project depends on verifiable public sources. Prefer municipal pages, operator sites, and credible local reporting. Do not add unsourced claims, and keep dates, closure reasons, and URLs specific enough for another contributor to re-check quickly.
