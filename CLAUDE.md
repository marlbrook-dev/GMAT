# Start From Nowhere: standing rules for every session

Owner: Hunter Roberts (admin emails: marlbrookgroup@gmail.com primary, hroberts@winthropcapital.com backup). Live site: startfromnowhere.com (Cloudflare Worker "gmat", deploys from main). Read ROADMAP.md for the current build schedule and src/blog/EDITORIAL.md for content rules before writing anything.

## Typography and layout

Nothing in this file is settled while the site is still being built. These are the
current decisions and the reasons behind them, not law: say so when one of them looks
wrong, and change it when the owner says to rather than quoting it back at them.

- Headers are Title Case everywhere: page titles, section headings (h1/h2/h3), nav labels, card titles, and buttons that name a destination or action ("Create Account", "Download CSV"). Small words (a, an, the, of, and, or, to, for, by, in, on, at, vs) stay lowercase unless first or last. Body copy, descriptions, and table cells stay sentence case.
- One system, defined once, in src/partials.py TOKENS_CSS and injected wherever {{CHROME_CSS}} goes. It holds the type scale
  (--t-100 to --t-900), the tracking ramp (--tr-900 to --tr-caps), a 4px spacing grid (--s1 to --s10), one page width, one gutter
  and one reading measure. Reach for a token before a number; a raw px value in a template is how the site ended up with 37 font
  sizes, 28 spacing values and eight page widths.
- Type tightens as it grows and never opens up: negative tracking on headings, scaling from -.032em at the hero to 0 at body size.
  The one positive value is .06em, for small uppercase labels, via the .eyebrow class.
- Grid and flex children need min-width:0. Without it they hold their min-content width and push the page sideways on a phone,
  which is what broke pricing, the rankings controls and the blog submit form.
- Three faces, no more. Source Serif 4 sets headings; IBM Plex Sans sets everything else, UI and body alike; IBM Plex Mono is for
  figures that sit in a column, never for words. The site used to run a fourth, Manrope, as a second sans beside IBM Plex Sans, and
  the two were close enough to read as a mistake. Sites that do this well run one sans and use the others sparingly: Stripe sohne
  100 declarations to 2 mono, Our World in Data Lato 396 to a display serif 117.
- The wordmark and logo are monochrome navy (#122B4E) and identical on every page; the wordmark always links to /.
- The site header (Exam Prep / Lists / Resources + Sign In + Create Account) is identical across landing, exams, schools, pricing, and blog pages. The trainer app keeps its own tab header, hidden during active sessions and games (focus mode).

## House style (hard rules, build fails on some of these)

- NO em dashes and NO en dashes anywhere: pages, posts, code strings, data files, commit messages.
- GMAT Focus (205 to 805) and Classic (200 to 800) are never converted or mixed; compare by percentile only (Classic 700 = Focus 655, 90.5th percentile, GMAC concordance).
- Never state a school statistic, price, or exam fact from memory. Every published figure carries source, year, and URL; unverifiable = null/dash, never a guess. Banned sources: GMAT Club, Quora, Wikipedia, GyanDhan, Pagalguy, forums, coaching-site blogs.
- Never fabricate product stats, user counts, testimonials, or efficacy claims. Personal bests, not leaderboards; accuracy-only game scoring, nothing luck-based.
- Blog: pen-name bylines with no invented credentials; never backdate; posts publish by date via the drip (one post every 2 days; daily publish cron).

## Never invent a value (owner's rule, non-negotiable)

- Every identifier, hash, ID, count, price, date, URL and statistic that goes into a tool
  call, a commit, a page or a message must be READ from a real output first: a command
  result, a file, a tool response. Never type one from memory, pattern, or plausibility.
  On 2026-09-19 a 40 character hex string was typed straight into a GitHub merge call as
  if it were a commit SHA. The API rejected it as malformed, which was luck; a
  well-formed guess would have merged something else.
- If the real value is not to hand, run the command that produces it (git rev-parse, a
  read, a query). That costs one tool call. Guessing costs correctness.
- This is the same rule as the sourcing rule below, applied to machine values instead of
  published figures, and it fails the same way: a number that looks right is the hardest
  kind of wrong to catch.

## The build playbook (write the record before you fix the bug)

- When something breaks, append a record to data/playbook/incidents.jsonl BEFORE fixing
  it, while you still remember what you believed was true five minutes ago. That belief is
  the actual defect and it is the first thing you lose. The record needs what was seen,
  why, how it surfaced, the fix, the guard that now catches it, and the lesson stated so
  it makes sense to someone who has never seen this code.
- python3 src/build_playbook.py regenerates the whole deliverable from those records: the
  book in playbook/ as Markdown, HTML, PDF and Word, the generated checklist, the analysis
  chapter, and the bootstrap pack for seeding a new project. Nothing is copied by hand, so
  writing the record is the only step.
- python3 src/playbook_harvest.py says which commits look like they describe a defect the
  ledger does not have. A weekly workflow runs it and opens an issue. If a flagged commit
  carries no real defect, put it in data/playbook/cleared.jsonl with a reason rather than
  skipping it silently: the ledger is the place that remembers what was looked at.
- playbook/ and docs/ are excluded from the deploy. The ledger is a list of this
  platform's historical weaknesses with the commits that fixed them.

## Communication (owner's rule, non-negotiable)

- If a link, site, or service cannot be accessed (egress blocked, login wall, rate limit, anything), say so IMMEDIATELY and ask how to proceed BEFORE doing the work another way. Never quietly substitute partial information (a screenshot, memory, a guess) for the source the owner pointed to. The owner always wants to know when there is a problem or a failed connection, at the moment it happens.

## Engineering workflow

- Develop on the designated claude/* branch; ship via PR to main, squash merge; main deploys the live site via Cloudflare Workers Builds.
- The Worker is no longer assets only: src/worker.mjs sits in front and 301s www.startfromnowhere.com to the apex, because localStorage is per origin and two hostnames meant two consent states and a split ranking signal. assets.run_worker_first must stay true or the asset router answers first and the redirect never runs. assets.directory is the repository root, so .assetsignore is the only thing keeping src/, data/, supabase/ and the internal docs from being served as part of the site; anything the built pages reference must stay out of it.
- python3 src/build.py builds everything (both trainer apps, landing, rankings, exams, pricing), node-parses every inline script, and fails on an em or en dash in any hand-edited doc or bank; cd src && node test.js runs engine tests once per exam; node src/smoke_items.js renders and grades one item from every generator schema at phone width, node src/smoke_consent.js covers consent and item telemetry, node src/smoke_billing.js covers the billing promises, node src/smoke_redirect.js asserts the www to apex redirect and that the deploy still excludes the source of the site, node src/smoke_guide.js renders every study guide page at phone and desktop width and fails on sideways scroll or a section that rendered empty; node src/review_bot.js runs one independent review bot per exam, which sits its own exam repeatedly against the real engine and reports what only playing reveals (estimate recovery, band coverage, whether selection actually adapts, bank reach, starving skills, and whether a planted weakness is diagnosed); src/exam_harness.js is the single place that knows each exam's bank files, shared by test.js and the bots so the two cannot drift; validate in headless Chromium (executablePath /opt/pw-browsers/chromium-*/chrome-linux/chrome) before shipping.
- Two exams are live and share one engine and one UI template: GMAT Focus at /app/ and the digital SAT at /sat/app/. src/engine.js holds the EXAMS registry and SKILLS / SECTION_META resolve from the EXAM_ID the build injects, so never hardcode a section key ('Q', 'RW') in app_template.html; use SECTIONS and SECTION_META. Adding an exam is a registry entry plus a tagged bank, a deck, a playbook, and entries in build.py APPS, test.js, build_exams.py LIVE and APP_PATH, and partials.py nav (steps in README).
- Score estimates: both trainers report an estimated range on the exam's own scale (GMAT Focus 205 to 805, SAT 400 to 1600), never a single number, never called a predicted score, and never shown before the evidence floor in EXAM.scale.minAttempts. The band half-width is the standard error of the ability estimate with a 30-point floor. The owner decided on 2026-09-16 to use each exam's scale after previously ruling the SAT out; the method, and the fact that the scale anchoring is our calibration rather than the test maker's, is published at /scoring/ and must stay in step with src/engine.js.
- Still true and not negotiable: never present our 60 percent SAT module routing cut as official, keep every structural fact sourced (see the Exam Content Sources section of data/DATA.md), and never claim or imply the estimate predicts a real score.
- Generated outputs are gitignored (/app/, /blog/, /schools/, /exams/, /pricing/, /community/, index.html, 404.html, terms.html, privacy.html, sitemap.xml); sources of truth live in src/ and data/.
- School library: one file per school in data/schools/ (schema and source ladder in data/DATA.md); src/validate_schools.py enforces source, year, and URL on every figure at build time and fails on banned sources, mixed GMAT editions, or implausible values. Add or fix a school by editing its file only.
- Shared site header and footer live in src/partials.py and are injected into every page at build time via {{SITE_HEADER}} / {{SITE_FOOTER}} / {{CHROME_CSS}}; never hand-edit chrome in a single template.
- JS-in-string onclick handlers must escape single quotes (this class of bug once took down the whole app; the build guard catches it).
- Supabase project: ftsqwbzhkzuudogkvoqa. Payments: Stripe Checkout only, live account acct_1UGMl23VQZ93CQqj. Plus $4.99/mo or $49.99/yr, Pro $9.99/mo or $99.99/yr, 7-day free trial on every paid plan. PAYMENTS_LIVE=true; FREE_LIMITS_LIVE stays false until the owner decides what grandfathering means for early users. Never commit a Stripe secret key or webhook signing secret; they live only in Supabase Edge Function secrets.
- Billing promises are load-bearing; do not weaken them in copy or code. The free plan never asks for a card (src/smoke_billing.js tests this in both auth states). Cancelling a Stripe subscription is one click in Account > Plan and Billing and runs through the cancel-subscription function, never through the Stripe portal, so it works whether or not the portal is configured. An Apple sourced subscription is the one exception and it is not ours to change: Apple owns it, offers no API to cancel on a user's behalf, and its guidelines require apps to point to Settings. So the button opens Apple's subscription management and says why, rather than appearing to work and not. Which path applies is decided by entitlement().managed_by, never guessed from the platform the page happens to be open on. Refunds only inside 72 hours of a charge, except our own billing errors, which are always refunded. Access continues to the end of the paid period. Billing contact is billing@startfromnowhere.com.
- Five edge functions: create-checkout-session, stripe-webhook (verify_jwt=false, Stripe signature instead), cancel-subscription, create-portal-session, and apple-notifications (verify_jwt=false, Apple JWS instead). Apple does not order notifications any more than Stripe does, so apple-notifications re-reads the subscription from the App Store Server API and writes current state rather than the payload, guards on signedDate, and treats refund and revoke as terminal. profiles.plan stays Stripe owned; entitlement() derives the effective plan across every source and is what the app reads. Neither cancel nor portal ever takes an id from the request body; both read it from the caller's RLS-scoped profiles row. Stripe does not order webhook events, so subscription handlers re-read the subscription and write current state rather than the event payload.
- Postgres grants: revoking EXECUTE from anon or authenticated does nothing while PUBLIC still holds it (look for a leading `=X/postgres` in pg_proc.proacl). Always revoke from PUBLIC too, and re-run the Supabase advisors afterwards rather than trusting the per-role grants.
- Sentinel (DEVSECOPS.md): partials.sentinel_js() ships an error beacon with the footer on every page, writing to client_errors (insert-only, no select policy, salted IP hash by trigger). Admin > Errors clusters them with evidence and a human marks each real, fixed, wont fix, or noise. Nothing in it edits code, and that is deliberate. Keep privacy.html in step with anything it starts collecting.
- Community forum (/community/, src/community.html): tables forum_categories / forum_threads / forum_posts with RLS (public read of non-hidden rows; open insert for anon and authed, user_id stamped server-side). Posting needs no account: named or anonymous with a stable per-device pseudonym; a 3-step wizard guides new threads. DB triggers stamp country + salted IP hash (raw IP never stored), enforce rate limits, and run forum_screen() rules (severe hits auto-hide, the rest flag); humans decide in the app's Admin > Moderation tab (admin_mod_queue / admin_moderate RPCs). Never seed fake member activity; SFN Team posts are the only house-authored content and say so.
- Analytics: every page carries the first-party beacon writing to site_events (sessionStorage sid, path, ref, utm, device, duration; country + salted IP hash added by trigger). No select policy on site_events; admins read via admin_traffic/admin_users/admin_user_detail RPCs (all is_admin-gated). Demographics are self-reported on the Account page and never inferred from behaviour. Since 2026-09-19 the owner's decision is that third-party attributes may also be bought and appended, on accounts recorded as 18 or over only: they live in profile_appended, never in the profiles columns, so what a person told us stays distinguishable from what we were sold about them; they are deleted when an age is corrected below 18 and by Delete Everything; and they are disclosed in privacy.html section 2 before any of it happens. Nothing is ever bought about anyone under 18. Disclosures live in privacy.html; keep them in sync with any collection change.
