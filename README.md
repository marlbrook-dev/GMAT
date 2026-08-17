# Start From Nowhere

Adaptive test-prep platform. First exam: GMAT Focus Edition (Quant, Verbal, Data Insights). Per-skill Elo ratings keyed to the official score-report skill labels, spaced repetition of misses, timing diagnostics, error log, playbook. Single-file app, no build tooling beyond Python.

## Layout
- `src/` — sources. `bank_*.js` (question banks), `engine.js` (exam-agnostic adaptive engine + exam registry), `app_template.html` (trainer UI), `landing.html` (marketing homepage), `build.py` (assembles the site), `build_blog.py` + `blog/` (The Study Room blog content and generator), `test.js` (bank validation and engine simulation)
- `design/` — Start From Nowhere design system (tokens, components, guidelines, UI kits). Source of truth for UI. SEO content rules: `design/guidelines/seo-content.md`
- `supabase/` — schema and setup notes for project meridian-prep
- `_headers`, `robots.txt` — Cloudflare Pages config
- Generated, not committed (see `.gitignore`): `index.html` (landing), `app/index.html` (trainer), `404.html`, `blog/`, `sitemap.xml`

## Develop
`python3 src/build.py && python3 src/build_blog.py` then open `index.html`. Run `node src/test.js` from `src/` to validate the bank and simulate the engine.

## Deploy
Cloudflare Pages: Workers & Pages > Create > Pages > Connect to Git > this repo.
Build command: `python3 src/build.py && python3 src/build_blog.py` — Output directory: `/` (build outputs land in the repo root).

## Roadmap
Done in Phase 4 so far: mock section mode (full 45-minute sections with review + 3 answer edits), The Study Room blog, privacy page, Stripe Checkout scaffold (edge functions deployed; set keys and flip `PAYMENTS_LIVE` to go live, see `supabase/README.md`).
Remaining: owner admin view on `item_stats`, match games, AI-generated variants, Stripe go-live, Google sign-in, weekly digest, more exams via the exam registry.
