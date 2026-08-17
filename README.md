# Meridian Prep

Adaptive test-prep trainer. First exam: GMAT Focus Edition (Quant, Verbal, Data Insights). Per-skill Elo ratings keyed to the official score-report skill labels, spaced repetition of misses, timing diagnostics, error log, playbook. Single-file app, no build tooling required.

## Layout
- `index.html` (and `404.html`) — the built app, served by Cloudflare Pages
- `src/` — `bank_*.js` (question banks), `engine.js` (exam-agnostic adaptive engine + exam registry), `app_template.html` (UI), `build.py` (concatenates into `index.html`), `test.js` (bank validation and engine simulation)
- `design/` — Meridian Prep design system (tokens, components, guidelines, UI kits). Source of truth for UI.
- `_headers`, `robots.txt` — Cloudflare Pages config

## Develop
`python3 src/build.py` then open `index.html`. Run `node src/test.js` from `src/` to validate the bank and simulate the engine.

## Deploy
Cloudflare Pages: Workers & Pages > Create > Pages > Connect to Git > this repo > Build command empty > Output directory `/`.

## Roadmap
Phase 2: 300+ item bank, flashcards + FSRS spaced review, timed sprint, progress calendar, GI/TA formats. Phase 3: accounts and sync (Supabase), mock sections, match games, AI-generated variants, more exams via the exam registry.
