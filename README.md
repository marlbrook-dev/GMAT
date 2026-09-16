# Start From Nowhere

Adaptive test-prep platform. Two exams live: GMAT Focus Edition (Quantitative Reasoning, Verbal Reasoning, Data Insights) and the digital SAT (Reading and Writing, Math). Per-skill Elo ratings keyed to each exam's official score-report labels, spaced repetition of misses, timing diagnostics, error log, playbook. Single-file app per exam, no build tooling beyond Python.

## Exams

One engine, one template, one app per exam. `engine.js` holds an `EXAMS` registry; `SKILLS` and `SECTION_META` resolve from whichever `EXAM_ID` the build injects, so adding an exam means a registry entry plus a tagged bank, not a fork of the UI.

| Exam | App | Sections | Adaptivity | Tracked skills |
| --- | --- | --- | --- | --- |
| GMAT Focus Edition | `/app/` | Q, V, DI at 45 minutes each | per question | 12 official score-report skills |
| SAT | `/sat/app/` | Reading and Writing 2 x 27 in 32 min; Math 2 x 22 in 35 min | per module, module 2 routed by module 1 | 8 official content domains |
| GRE General Test | `/gre/app/` | Verbal and Quantitative, two unequal modules each (12 then 15) | per module, module 2 routed by module 1 | 7 content areas, plus an Analytical Writing task |

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

## Item banks: written and generated

Two kinds of bank feed every app.

- **Hand written** banks live in `src/bank_*.js` and are the source of truth for
  passage based and argument based items.
- **Generated** banks come from the schemas in `src/gen/`. `src/build_banks.py` runs
  them into `src/generated/bank_gen_<exam>.js`, which is build output and gitignored;
  the schemas are the source of truth. The run is seeded, so the same commit always
  produces the same bank.

A schema never asserts an answer. It draws parameters, computes the answer in Python,
and builds each distractor from a named misconception that the item's explanation then
names back. Anything failing self check on the way out is dropped and counted.

Three properties the framework enforces, each closing a way to score above chance
without reading the question:

- choice sets are homogeneous, so a lone fraction among integers cannot give the key away
- the key's rank among the values is drawn uniformly, so neither the largest nor the
  smallest option carries information
- distractors include numbers lifted from the stem, because errors that inflate a value
  are easier to write than errors that shrink one

`src/test.js` measures both axes **per section** and holds recorded numbers in `DEBT`
as a ratchet. Per section matters: adding 500 unbiased items once moved a failing
aggregate into tolerance without a single biased item changing.

## Payload

The item bank ships as `bank.js` next to each `index.html`, not inlined, so the shell
stays around 277k and the two cache separately. If the bank fails to load the app says
so rather than rendering blank. Test the apps over HTTP, not `file://`; the bank path is
absolute because the GMAT app doubles as `404.html`.

## Adding an exam
1. Add an entry to `EXAMS` in `src/engine.js`: sections (name, short, per-question pace,
   questions, minutes), skills keyed to that exam's official score-report labels, score
   scales, answer choice count, and a `scale` block if the app reports a band.
2. Write banks tagged with those section and skill ids. Item ids need their own prefix so
   the build can count them separately.
3. Write a flashcard deck and a playbook file for the new skills.
4. Add the exam to `APPS` in `src/build.py` (bank files, concat expression, `gen` key,
   trademark footer) and to the exam list in `src/test.js` (including its `gen` key, and a
   `choicesByType` entry if any item type uses a different number of choices).
5. Mark it live in `LIVE` and `APP_PATH` in `src/build_exams.py`, and in the header groups
   in `src/partials.py`.
6. For generated content, either map existing schemas onto the new taxonomy in
   `src/gen/mapping.py` or write new ones, then add the plan to `src/build_banks.py`.
7. A module adaptive exam needs enough easy items to fill a routed down module. Check the
   "easier-module pool" line `test.js` prints; short pools are why `bank_sat_easy.js` and
   `bank_gre_easy.js` exist.
8. Add the exam's item count to `_ALLOWED_COUNTS` in `src/build.py` or the count guard will
   fail the next time a page advertises the number.

## Roadmap
See `ROADMAP.md` for the current schedule. Open items include the Stripe go-live checkpoint (`PAYMENTS_LIVE`), SFN Assist AI coaching, an undergraduate rankings vertical to pair with the SAT trainer, and GRE and LSAT builds through the same exam registry.
