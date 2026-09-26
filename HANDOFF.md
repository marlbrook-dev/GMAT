# Start From Nowhere: handoff

Written 2026-09-19. Everything below is either measured or read from the repo. Where a
number is stale by the time you read it, the build will tell you: it checks the counts
quoted in `llms.txt` and `src/blog/EDITORIAL.md` against reality and fails if they drift.

Read `CLAUDE.md` first. It holds the standing rules and it is the file that overrides
this one. This document is orientation and open work; that one is law, except where it
says it is not, which it says at the top of its own typography section.

---

## What this is

A test-prep site at **startfromnowhere.com**. Five adaptive trainers sharing one engine
and one UI template, plus sourced rankings, exam guides, a blog, and a forum. Static
pre-rendered HTML on Cloudflare Workers, deployed from `main`. Supabase for auth, sync,
analytics and billing. Stripe for payments, live.

The thing that distinguishes it from the rest of the category is that every published
figure carries a source, a year and a URL, and unverifiable means a dash rather than a
guess. That is not a style preference, it is the product. Breaking it is the one change
that makes the site worth less than the sum of its pages.

### Live today

| Trainer | Path | Items |
|---|---|---|
| GMAT Focus | `/app/` | 27,914 |
| ACT | `/act/app/` | 36,745 |
| Digital SAT | `/sat/app/` | 17,116 |
| GRE | `/gre/app/` | 19,914 |
| LSAT | `/lsat/app/` | 372 |

**102,061 items total.** Also live: `/colleges/` (1,451 colleges, four ranked categories),
`/schools/` (91 MBA programs), `/exams/`, `/blog/` (29 posts, drip publishing), `/apply/`,
`/community/`, `/funding/`, `/international/`, `/scoring/`, `/pricing/`, `/do-not-sell/`.

MCAT and Executive Assessment were removed on 2026-09-18: their source material is not
reachable from this environment, and the house rule forbids publishing exam facts without
a source.

---

## Build and test

```
python3 src/build.py          # everything: trainers, landing, rankings, exams, pricing
python3 src/build_blog.py     # blog and sitemap
cd src && node test.js        # engine tests, once per exam
```

Browser suites, all needing `CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome`:

| File | What it guards |
|---|---|
| `src/smoke_items.js` | 182 generated schemas render and grade at phone width |
| `src/smoke_load.js` | time to first question, unthrottled and on throttled 3G |
| `src/smoke_signup.js` | the age gate is present and required, across all five trainers |
| `src/smoke_sharing.js` | eight Account-card states, the Do Not Sell page, policy consistency |
| `src/smoke_consent.js` | consent gating and item telemetry |
| `src/smoke_funnel.js` | the analytics beacon actually fires |
| `src/smoke_billing.js` | the free tier never asks for a card; billing copy per state |
| `src/smoke_rankings.js` | rankings filters and interaction |

`src/sql/smoke_sharing.sql` covers the database guarantees. It always ends by raising,
which rolls the whole thing back, so the results arrive in the error message and nothing
synthetic survives. Confirm afterwards with a count on
`auth.users where email like '%@example.invalid'`.

The build enforces several house rules itself and exits non-zero: no em or en dashes
anywhere, every inline script must parse under `node --check`, no unresolved `{{...}}`
placeholders, and the item and price counts quoted in docs must match reality.

---

## Architecture, and the parts that will surprise you

### One engine, five exams

`src/engine.js` holds the `EXAMS` registry. `SKILLS` and `SECTION_META` resolve from the
`EXAM_ID` the build injects. **Never hardcode a section key** like `'Q'` or `'RW'` in
`app_template.html`; use `SECTIONS` and `SECTION_META`. Adding an exam is a registry
entry, a tagged bank, a deck, a playbook, and entries in `build.py` `APPS`, `test.js`,
`build_exams.py` `LIVE` and `APP_PATH`, and `partials.py` nav. Steps are in `README.md`.

### The item bank ships in two pieces

`src/gen/` holds generator schemas; they are the source of truth and the emitted `.js` is
build output, gitignored like `/app/` and `/blog/`. `build_banks.py` runs them, seeded
with `zlib.crc32` so the same commit always produces the same bank. It must not use
Python's `hash()`, which is randomised per process and quietly made every build different.

`TARGET` in `build_banks.py` is items per category, currently 1200. Three categories
exhaust their parameter space below that and ship at their own ceiling, named in a comment
there: `gmat/v_pc` 833, `sat/rw_eoi` 971, `act/act_e_pow` 974.

Each bank emits as `bank.js` (blocking) and `bank_rest.js` (async). The blocking file
carries every hand-written item plus 80 per skill of the generated ones, **strided** rather
than taken from the front, because generator output is sequential and the front of a run
is not spread across difficulty. The async file pushes the remainder into the same array
and calls `window.__bankGrew` to reindex. `const` forbids reassignment, not mutation,
which is what makes that work.

This exists because on regular 3G the whole-bank blocking script took 20.3s to first
question for GMAT and 23.4s for ACT. It is now 11.0s and 7.6s. **If you grow the bank
again, run `src/smoke_load.js` and look at the 3G row**, not the unthrottled one, which
flatters a megabyte badly.

### Design tokens

One system, defined once, in `src/partials.py` `TOKENS_CSS`, injected wherever
`{{CHROME_CSS}}` goes. Type scale `--t-100` to `--t-900`, tracking ramp, a 4px spacing
grid, one page width, one gutter, one reading measure. Reach for a token before a number.
Shared header and footer live in the same file and inject via `{{SITE_HEADER}}` /
`{{SITE_FOOTER}}`; never hand-edit chrome in a single template.

### Data model

Supabase project `ftsqwbzhkzuudogkvoqa`. Migrations live in `supabase/migrations/`.

**`profiles`** carries account data, self-declared demographics, billing state, and the
age and sharing columns. Four `BEFORE` triggers run on it and **the order is load-bearing**,
which is why they are named `profiles_trg_0` through `profiles_trg_3`:

| Trigger | Does |
|---|---|
| `trg_0_signup_country` | stamps `signup_country` from `cf-ipcountry` at insert |
| `trg_1_sync_age_tier` | derives `age_tier` from `birth_year` / `birth_month` |
| `trg_2_sharing_eligibility` | revokes sharing when the tier is not `18_plus` |
| `trg_3_purge_appended` | deletes purchased attributes when the tier drops below 18 |

**`item_events`** is deliberately unlinkable: no user, session, device or IP column exists,
so a row cannot be tied to a person or to another row. That is why it is not behind the
consent banner, and the banner says so rather than hiding it. Do not add an identifying
column to it, ever, without changing the privacy policy first.

**`site_events`** is the opposite: consent-gated, with a session id and a salted IP hash
added by trigger. No select policy; admins read through `is_admin`-gated RPCs.

---

## The data sharing programme

This is the part with the most legal surface and the most recent churn, so read it before
touching anything near it.

The owner's decision is that the site sells first-party data and buys third-party data
about its own users. Both are built. The shape:

- **Selling is opt-out for adults** outside the EEA, the UK and Switzerland, which is what
  CCPA permits given notice and a Do Not Sell link, both of which exist. Inside those
  places GDPR offers no opt-out for this, so sharing stays off until the person says yes.
  Basis comes from `signup_country`, never from the self-declared `country` field, because
  a legal basis you can change by typing in a box is not one. Unknown country counts as
  consent-required.
- **Nothing about anyone under 18, ever.** Not sold, not shared, not bought, not appended.
  Enforced in the database: an account under 18 cannot appear in `sellable_profiles`, and
  `profile_appended` refuses the insert outright.
- **Accounts created before the policy are excluded.** They were told we would never sell.
  `sellable_profiles` filters `created_at` against the policy start date. Under the old
  opt-in model this was belt and braces; under opt-out it is the only thing standing
  between a changed default and selling data collected under the opposite promise.
- **Opting out stops the sale and nothing else.** Data is still collected, still runs the
  adaptive engine, and attributes can still be appended. It just cannot be exported.
- **Purchased attributes live in `profile_appended`, never in the `profiles` columns.**
  Three reasons that are one reason: a deletion request cannot reach what it cannot tell
  apart; the policy says those fields are self-declared and that must stay true; and when
  a broker's data is wrong you need to drop that source without touching what the person
  told you.

`sellable_profiles` is the only view an export may read, and `sellable_profiles_enriched`
adds the purchased attributes. They are two views on purpose: reselling bought data is a
different business from selling what your own users told you, and the line is close enough
that crossing it should be visible in the schema rather than buried in a join.

**The Do Not Sell link is not a concession.** CCPA §1798.135(a) requires any business that
sells to publish it. It is the permission slip. It is in the footer of every page including
the rankings index, which builds its own chrome and was the one page that nearly missed it.

### Current cohort

**1 account. Age undeclared. 0 sellable. 0 appended.** The machinery is correct and the
cohort is empty because the site is new. The one existing account predates the policy, so
it is excluded on the retroactive rule and stays excluded unless that person opts in.

Worth knowing before planning: the programme is adults-only, so GMAT, GRE and LSAT feed an
eligible cohort and SAT and ACT feed a permanently excluded one. Three of five trainers can
ever contribute. Your exam mix, not your opt-out rate, sets the ceiling.

---

## Open work, in the order I would do it

### 1. The reading corpus. This is the biggest real gap.

Every thin category is passage-based reading, because passages are hand-written and no
generator makes them:

```
GRE  gre_rc            14
ACT  act_r_kid 18, act_r_cs 11, act_r_iki 11
LSAT reading, 10 to 20 per category; Logical Reasoning is now 29 to 31
```

Maths categories hold 1,200 each. A student who picks reading exhausts it in one sitting.
The headline of 101,336 is honest and the items are real, but the distribution is not, and
**no increase to `TARGET` will change this**. It needs written passages with item sets.
This is the work that would most improve the product.

### 2. Under-13 accounts and COPPA

Today an under-13 account can exist and the trainer collects from it. COPPA requires
verifiable parental consent to collect personal information from a child under 13 at all,
and that obligation attaches on collection, not on selling, so it stands regardless of the
sharing programme. The age gate now records the tier, which means you can see the problem;
it does not yet act on it. Either block under-13 signups or build a parental consent path.
Which one is a business call, not a technical one.

### 3. Three migrations are not in the repo

Applied straight to the project on 2026-09-18 and never written into
`supabase/migrations/`, so the schema cannot be rebuilt from source alone:
`age_gate_and_data_sharing_consent`, `birth_month_year_second_layer`,
`data_sharing_export_and_profile_fields`. The gap is named at the top of
`supabase/migrations/20260918_data_sharing_programme.sql`. Reconstruct from the live
schema, verify by diffing a fresh apply, and delete that header note.

### 4. Bank scraper protection

The 101,336-item bank is the asset worth defending. Cloudflare is already in front. Add
AI-crawler directives to `robots.txt` (GPTBot, ClaudeBot, CCBot, Google-Extended,
PerplexityBot, Bytespider), turn on bot management against the `bank.js` and
`bank_rest.js` endpoints, and match it in `terms.html`. Keep content pages fully
crawlable: the point is to stop bulk bank extraction, not indexing.

### 5. Settings the owner has to do, not you

- Authorize the Cloudflare connector, so deploy status can be read directly rather than by
  polling live URLs.
- Turn on leaked-password protection in Supabase Auth.

### Smaller, still open

- Scholarship sourcing, column and articles (task 15).
- The LSAT bank is 282 items and says so on its own page rather than implying more. Logical
  Reasoning is now 29 to 31 per skill; the five reading skills are still 10 to 20 and are
  what the review bot warns about.

---

## Traps this codebase has actually sprung

Each of these cost real time. They are here so they cost you none.

**CSS comments do not nest.** The first `*/` closes the outer comment. A `{{CHROME_CSS}}`
placeholder left inside an opening comment in `rankings_base.css` killed the colour palette
on 1,451 pages and looked like a design problem for hours.

**Grid and flex children need `min-width:0`.** Without it they hold their min-content width
and push the page sideways on a phone. This broke pricing, the rankings controls and the
blog submit form, separately.

**`overflow:hidden` makes an element the scroll container that `position:sticky` resolves
against.** A sticky header that will not stick usually means an ancestor got `overflow`.

**Postgres fires same-timing triggers alphabetically.** `profiles_sharing_eligibility`
sorted before `profiles_sync_age_tier`, so eligibility was judged against a stale age tier
and silently revoked every legitimate adult opt-in. Hence the numeric prefixes.

**`UPDATE OF <columns>` fires on the columns named in the statement**, not on what changed
and not on what an earlier `BEFORE` trigger wrote into `NEW`. So
`update profiles set birth_year = 2011` ran the sync, stored a minor's tier, and skipped
the eligibility check entirely.

**Revoking `EXECUTE` from `anon` or `authenticated` does nothing while `PUBLIC` still holds
it.** Look for a leading `=X/postgres` in `pg_proc.proacl`. Always revoke from `PUBLIC` too,
and re-run the Supabase advisors afterwards rather than trusting per-role grants.

**`const BANK` is a lexical global, not a `window` property.** Other classic scripts can see
it; `window.BANK` is undefined. This is what makes the two-stage bank load work.

**JS-in-string `onclick` handlers must escape single quotes.** This class of bug once took
down the whole app. The build guard catches it now.

**A test can pass for the wrong reason.** `smoke_funnel` used storage key `sfn_consent`
instead of `sfn_consent_v1`, so "nothing sent on refusal" passed because nothing was
configured at all. Fixing the key exposed a real bug underneath. Similarly `smoke_load`
waited for the `load` event, which waits for the async bank, and would have reported no
improvement from a change that made the page usable nine times faster.

**A guard can silently narrow its own scope.** The build's item-count check matched
`\d{2,4}`. When the banks passed ten thousand, the two largest counts stopped matching the
pattern, and the guard would have kept passing while checking nothing.

---

## Rules that are not negotiable

From `CLAUDE.md`, restated because they are the ones most easily broken by accident:

- **No em dashes, no en dashes.** Anywhere. Pages, posts, code strings, data files, commit
  messages. The build fails on hand-edited files.
- **Never state a school statistic, price, or exam fact from memory.** Source, year, URL, or
  a dash. Banned sources: GMAT Club, Quora, Wikipedia, GyanDhan, Pagalguy, forums,
  coaching-site blogs.
- **Never invent a value.** Every identifier, hash, ID, count, price, date and URL must be
  read from a real output before it is used. This rule exists because on 2026-09-19 a
  40-character hex string was typed into a GitHub merge call as if it were a commit SHA.
  The API rejected it as malformed, which was luck; a well-formed guess would have merged
  something else.
- **Never fabricate product stats, user counts, testimonials or efficacy claims.** Personal
  bests, not leaderboards.
- **Say immediately when something cannot be reached.** Egress blocked, login wall, rate
  limit, anything. Do not quietly substitute memory or a guess for the source the owner
  pointed at. This is the owner's rule and it is the one they care most about.
- **GMAT Focus (205 to 805) and Classic (200 to 800) are never converted or mixed.** Compare
  by percentile only.
- **Score estimates are ranges, never a single number, never called a prediction**, and never
  shown before `EXAM.scale.minAttempts`. The method is published at `/scoring/` and must stay
  in step with `src/engine.js`.
- **The free plan never asks for a card.** `smoke_billing.js` tests this in both auth states.
- **Never commit a Stripe secret key or webhook signing secret.** They live only in Supabase
  Edge Function secrets.
- **Keep `privacy.html` in step with anything the site starts collecting.** A policy that
  describes one thing while the database does another is worse than either alone.
- **Never seed fake member activity** in the forum. SFN Team posts are the only
  house-authored content and they say so.

---

## Where things live

```
src/partials.py        shared header, footer, design tokens, consent banner, sentinel
src/app_template.html  the one trainer UI, all five exams
src/engine.js          EXAMS registry, adaptive engine, scoring
src/build.py           builds everything; holds APPS and the house-rule guards
src/build_banks.py     runs the generators; TARGET and the starter split live here
src/gen/               generator schemas, the source of truth for items
src/sql/               database tests that roll themselves back
data/schools/          one file per MBA program
data/DATA.md           schema and the source ladder
supabase/migrations/   schema history, with one known gap
CLAUDE.md              standing rules; overrides this file
ROADMAP.md             build schedule
src/blog/EDITORIAL.md  content rules and the fact sheet writers work from
```

Generated output is gitignored: `/app/`, `/blog/`, `/schools/`, `/exams/`, `/pricing/`,
`/community/`, `/colleges/`, `/do-not-sell/`, `index.html`, `404.html`, `terms.html`,
`privacy.html`, `sitemap.xml`, and `*/bank_rest.js`. Sources of truth are in `src/` and
`data/`.
