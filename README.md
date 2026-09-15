# Start From Nowhere

Adaptive test-prep platform. Two exams live: GMAT Focus Edition (Quantitative Reasoning, Verbal Reasoning, Data Insights) and the digital SAT (Reading and Writing, Math). Per-skill Elo ratings keyed to each exam's official score-report labels, spaced repetition of misses, timing diagnostics, error log, playbook. Single-file app per exam, no build tooling beyond Python.

## Exams

One engine, one template, one app per exam. `engine.js` holds an `EXAMS` registry; `SKILLS` and `SECTION_META` resolve from whichever `EXAM_ID` the build injects, so adding an exam means a registry entry plus a tagged bank, not a fork of the UI.

| Exam | App | Sections | Adaptivity | Tracked skills |
| --- | --- | --- | --- | --- |
| GMAT Focus Edition | `/app/` | Q, V, DI at 45 minutes each | per question | 12 official score-report skills |
| SAT | `/sat/app/` | Reading and Writing 2 x 27 in 32 min; Math 2 x 22 in 35 min | per module, module 2 routed by module 1 | 8 official content domains |

SAT specifics: four answer choices rather than five, student-produced responses (grid-ins) graded by value so 1/2, 0.5 and .5 all count, free answer changes inside a module, and a section report that breaks results out by module and by content domain. Nothing in the app reports a 400 to 1600 score; College Board's equating tables are not public, so the app reports accuracy, per-domain results, and which second module you routed into.

## Layout
- `src/`: sources. `bank_*.js` (GMAT banks), `bank_sat_*.js` (SAT banks), `cards*.js` / `cards_sat.js` (flashcard decks), `playbook_gmat.js` / `playbook_sat.js` (method notes per skill), `engine.js` (exam-agnostic adaptive engine + exam registry), `app_template.html` (trainer UI, built once per exam), `landing.html` (marketing homepage), `build.py` (assembles the site), `build_blog.py` + `blog/` (The Study Room blog content and generator), `test.js` (bank validation and engine simulation, run per exam)
- `design/`: Start From Nowhere design system (tokens, components, guidelines, UI kits). Source of truth for UI. SEO content rules: `design/guidelines/seo-content.md`
- `supabase/`: schema and setup notes for project meridian-prep
- `_headers`, `robots.txt`: Cloudflare Pages config
- Generated, not committed (see `.gitignore`): `index.html` (landing), `app/index.html` and `sat/app/index.html` (trainers), `404.html`, `blog/`, `sitemap.xml`

## Develop
`python3 src/build.py && python3 src/build_blog.py` then open `index.html`. Run `node test.js` from `src/` to validate every bank and simulate the engine once per exam; it checks answer keys in both directions, SAT module construction against College Board's published domain ranges, and grid-in equivalence.

## Deploy
Cloudflare Workers (Git-connected): Compute > Workers & Pages > Create > import this repo.
Build command: `python3 src/build.py && python3 src/build_blog.py`. Deploy command: `npx wrangler deploy` (config in `wrangler.jsonc`; the built site is served as static assets from the repo root).

## Adding an exam
1. Add an entry to `EXAMS` in `src/engine.js`: sections (name, short, per-question pace, questions, minutes), skills keyed to that exam's official score-report labels, score scales, answer choice count.
2. Write banks tagged with those section and skill ids. Item ids need their own prefix so the build can count them separately.
3. Write a flashcard deck and a playbook file for the new skills.
4. Add the exam to `APPS` in `src/build.py` (bank files, concat expression, trademark footer) and to the exam list in `src/test.js`.
5. Mark it live in `LIVE` and `APP_PATH` in `src/build_exams.py`, and in the header groups in `src/partials.py`.

## Roadmap
See `ROADMAP.md` for the current schedule. Open items include the Stripe go-live checkpoint (`PAYMENTS_LIVE`), SFN Assist AI coaching, an undergraduate rankings vertical to pair with the SAT trainer, and GRE and LSAT builds through the same exam registry.
