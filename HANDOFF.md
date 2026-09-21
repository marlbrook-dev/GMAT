# Handoff: Start From Nowhere, 2026-09-21

Paste the "Opening message" section below into a new chat. Everything above it is context
for you; everything in it is context for the next session.

---

## State as of this handoff

Live site: startfromnowhere.com, Cloudflare Worker "gmat", deploys from `main`.
Repository: `marlbrook-dev/GMAT`. Supabase project `ftsqwbzhkzuudogkvoqa` ("meridian-prep").
Stripe live account `acct_1UGMl23VQZ93CQqj`.

**`main` is at `c4698e0`** (squash merge of PR #52) and it is deployed and verified live.

### What shipped on 2026-09-21

All merged and confirmed serving on the live site:

1. **Per exam review bots** (`src/review_bot.js`). Each boots its exam and plays it against
   the real engine, answering with the engine's own `pCorrect` at each item's own difficulty.
   Reports estimate recovery, band coverage, whether the FIRST band shown is right, adaptivity,
   bank reach, starving skills, and whether a planted single-section weakness is diagnosed.
   `src/exam_harness.js` holds the bank file lists and VM boot, shared with `test.js`.

2. **The score estimator, rewritten.** It used to average per-skill Elo ratings. Two faults:
   untested skills voted (sitting at theta 0 with weight 1), and Elo moves too slowly to have
   gone anywhere after ~2 observations per skill. Section ability is now fitted directly to the
   attempts by Fisher scoring on the 3PL, weak N(0, 1.5) prior. Measured improvement, 25
   sittings per exam:

   | exam | band coverage | first band at floor | mean error |
   |---|---|---|---|
   | SAT | 20 to 76 pct | 32 to 72 pct | 140 to 73 |
   | GMAT Focus | 40 to 80 pct | 20 to 80 pct | 50 to 28 |
   | GRE | 36 to 72 pct | 28 to 72 pct | 9 to 5 |
   | LSAT | 40 to 84 pct | 20 to 76 pct | 7 to 4 |
   | ACT | 20 to 80 pct | 40 to 56 pct | 4 to 3 |

   `/scoring/` was rewritten to match, because it described the old method.

3. **Three live defects fixed.** The error beacon reported its own failures in a loop
   (`fetch` rejects, it does not throw, so the try/catch caught nothing and the rejection
   reached the `unhandledrejection` handler which called `report` again: 267 rows). The
   beacon recorded third party blocked scripts (1,202 of the first 1,490 rows were one
   Cloudflare beacon blocked by ad blockers). The evidence floor opened after 30 real items
   on a 40 item promise, because items carrying a `qskill` counted twice.

4. **Games.** Ordered per exam by a `gameplan` entry in the registry, with the reason on the
   card. Plus the study constellation: one node per skill, edges drawn only between adjacent
   mastered skills, six stages. It cannot be farmed, because a node lights only when
   `skillStats` calls a skill green, which needs rating, volume and accuracy together.
   Confetti and the constellation pulse now stop under `prefers-reduced-motion`.

5. **`src/weekly_audit.js`**, one command running build, blog, engine tests, review bots and
   the browser suites, printing regressions first and bot findings as the backlog.

### Traps this codebase has actually sprung

Worth knowing before touching anything:

- `fetch` rejects on network failure, it does not throw. A `try/catch` around it catches
  nothing. This shipped and put 267 junk rows in the error table.
- Postgres fires same-timing triggers **alphabetically**, hence the `profiles_trg_0/1/2/3`
  naming. Renaming one silently reorders behaviour.
- `UPDATE OF <columns>` fires on the columns NAMED in the statement, not on what changed, and
  not on what an earlier BEFORE trigger wrote into `NEW`.
- `PUBLIC` holds EXECUTE by default. Revoking from `anon`/`authenticated` alone does nothing.
  Look for a leading `=X/postgres` in `pg_proc.proacl`.
- CSS has no error for an undefined custom property. `var(--missing)` silently resolves to
  nothing, which is how the Do Not Sell page shipped with an invisible button.
- `TOKENS_CSS` defines type, spacing, radii and shadows, but **no colour tokens**. Every page
  declares its own `:root` palette.
- `localStorage` is per ORIGIN and ignores canonical tags. This is why the cookie dialog
  reappears (see below).
- The Worker redirects `.html` paths, so `curl` without `-L` hashes an empty body.

### The open bug you should fix first

**`www.startfromnowhere.com` serves 200 with no redirect to the apex.** Both hostnames serve
identical content. Because `localStorage` is per origin, consent accepted on one hostname is
invisible on the other, which is why the cookie dialog keeps reappearing. It also splits SEO
signals while the site sits at average position 25 to 42.

Fix: a Cloudflare 301 redirect rule. Not in this repository. Needs the Cloudflare connector,
which is authorised but only attaches in a NEW session. Details in `CONNECTORS.md`.

### Known defects still open

Measured by the review bots, 25 sittings per exam:

- ACT band coverage at the evidence floor is 56 percent, against 72 to 80 elsewhere. Its band
  is plus or minus 2 on a 1 to 36 scale, the tightest published, so this is a band floor
  question rather than an estimator question.
- 8 to 14 percent of served items repeat while unserved items remain in the same section.
- Adaptive selection barely separates ability tiers on GMAT Focus and the LSAT, because a
  realistic session never leaves calibration mode.
- The LSAT bank is 65 items and cannot sustain one 140 item sitting. Repeats there are
  arithmetic, not a defect. The fix is content.

### Search Console, read from the owner's export, 3 months to 2026-09-19

16,843 impressions, 9 clicks, CTR 0.05 percent. Average position improved from ~70 to ~25.
47 queries already rank at position 10 or better and they are all sourced school statistics
(class profiles, acceptance rates, tuition). 27 queries sit at position 8 to 20 with 439
impressions and **zero** clicks, which is a title and snippet problem and the cheapest win
available. Brand queries (school names) sit at 40 to 70 and are not winnable. The trainer
side has almost no organic reach: `/exams/gmat/` is at position 55.

---

## Opening message for the new chat

> I am continuing work on Start From Nowhere (startfromnowhere.com), repository
> `marlbrook-dev/GMAT`. Read `CLAUDE.md` first and follow it exactly, especially: never invent
> a value (read every id, hash, count and statistic from a real output first), no em or en
> dashes anywhere, never state a school or exam fact from memory, and tell me IMMEDIATELY if
> a service or link cannot be reached rather than working around it quietly.
>
> Read `HANDOFF.md` and `CONNECTORS.md` in the repository root for where things stand.
>
> `main` is at `c4698e0` and deployed. Develop on a `claude/*` branch and ship via draft PR.
>
> **First task: the Cloudflare www to apex redirect.** `www.startfromnowhere.com` serves 200
> with no redirect, and because `localStorage` is per origin that is why the cookie consent
> dialog keeps reappearing for me. It also splits SEO across two hostnames. The Cloudflare
> connector is authorised and should be available to you in this session. Confirm you can see
> it before starting, and tell me if you cannot. After the redirect, do a full Cloudflare
> optimisation pass: caching rules, Early Hints, Brotli, HTTP/3, image resizing, bot rules to
> protect the item bank.
>
> **Second task: the reporting layer.** This is the largest block of undelivered work and all
> of it is unblocked. In order: a reusable chart component set in the house type and colour
> system (time series, cohort, funnel, distribution, comparison, accessible in both themes and
> readable at 400px); then the business admin dashboard pulling revenue, MRR, trial conversion,
> churn and refunds from Stripe and Apple alongside traffic and funnel from `site_events`; then
> a CoStar style dataset builder where I pick dimensions, measures, filters and a date range,
> save the view, share it and export CSV; then report generation from a saved view; then a
> proper student facing dashboard.
>
> Run `node src/weekly_audit.js` before you start so you know the baseline, and again before
> you open the PR.
>
> The full outstanding scope, with deliverables and what blocks each one, is in
> `Start-From-Nowhere-Outstanding-Scope.docx` in this handoff bundle.
