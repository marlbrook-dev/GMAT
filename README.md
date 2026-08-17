# Meridian Prep

Adaptive test-prep platform. First exam: GMAT Focus Edition (Quant, Verbal, Data Insights). Per-skill Elo ratings keyed to the official score-report skill labels, spaced repetition of misses, timing diagnostics, error log, playbook. Single-file app, no build tooling beyond Python.

## Layout
- `src/` — sources. `bank_*.js` (question banks), `engine.js` (exam-agnostic adaptive engine + exam registry), `app_template.html` (trainer UI), `landing.html` (marketing homepage), `build.py` (assembles the site), `build_blog.py` + `blog/` (The Study Room blog content and generator), `test.js` (bank validation and engine simulation)
- `design/` — Meridian Prep design system (tokens, components, guidelines, UI kits). Source of truth for UI. SEO content rules: `design/guidelines/seo-content.md`
- `supabase/` — schema and setup notes for project meridian-prep
- `_headers`, `robots.txt` — Cloudflare Pages config
- Generated, not committed (see `.gitignore`): `index.html` (landing), `app/index.html` (trainer), `404.html`, `blog/`, `sitemap.xml`

## Develop
`python3 src/build.py && python3 src/build_blog.py` then open `index.html`. Run `node src/test.js` from `src/` to validate the bank and simulate the engine.

## Deploy
Cloudflare Pages: Workers & Pages > Create > Pages > Connect to Git > this repo.
Build command: `python3 src/build.py && python3 src/build_blog.py` — Output directory: `/` (build outputs land in the repo root).

## Roadmap
Phase 4: mock section mode, blog growth (see `design/guidelines/seo-content.md`), Stripe Checkout, more exams via the exam registry.
