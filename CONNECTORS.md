# Connector setup for Start From Nowhere

## Update, 2026-09-26

Checked in the session of 2026-09-26, each from a real tool response:

- **Cloudflare is attached and working.** The Workers list returns the `gmat` worker. The
  www to apex redirect that section 1 below asks for is done, in the repository rather than
  as a dashboard rule: `src/worker.mjs` answers www.startfromnowhere.com with a 301 to the
  apex, and `src/smoke_redirect.js` tests it.
- **Google Search Console through Supermetrics still reads NOT_AUTHENTICATED** for source
  `GW`. Section 2 below still applies: the owner connects `GW` in Supermetrics with the
  Google account that owns the property. Until then, Search Console questions need an
  export, which `src/gsc_report.py` reads.
- **The weekly audit Routine now carries connectors**: Cloudflare, Supabase, Supermetrics,
  Adobe, Figma, Stripe and Claude Docs. Its next run is 2026-09-28. The prompt's list of
  known open items dates from 2026-09-21; the www redirect in it is done, and the LSAT bank
  is no longer 65 items.

Everything below is the snapshot of 2026-09-21, kept as it was written.

---

Verified on 2026-09-21 by calling each connector's own identity or list endpoint. Anything
marked "verified" below was confirmed from a real tool response, not assumed.

**The single most important thing:** MCP connectors attach when a session STARTS. Authorising
one mid-conversation does not load it into the running session. If you authorise something,
start a new chat afterwards.

---

## Working now, nothing to do

| Connector | Verified as | Used for |
|---|---|---|
| **GitHub** | repo `marlbrook-dev/GMAT`, merged PR #52 | All code, PRs, CI |
| **Supabase** | project `ftsqwbzhkzuudogkvoqa` ("meridian-prep"), ACTIVE_HEALTHY, Postgres 17.6 | Database, migrations, edge functions, error and traffic telemetry, advisors |
| **Stripe** | `acct_1UGMl23VQZ93CQqj`, livemode true, "Start from Nowhere" | Billing, MRR, trial conversion, churn for the admin dashboard |
| **Figma** | Marlbrook Group, marlbrookgroup@gmail.com, admin on the team | Design system work, chart and dashboard layouts |
| **Microsoft 365** | Hunter Roberts, hroberts@winthropcapital.com | Documents, calendar, mail if needed |
| **Fathom** | Hunter Roberts | Meeting transcripts and summaries |

## Needs action

### 1. Cloudflare (highest priority)

**Status:** authorised by you on 2026-09-21, but NOT reachable in the session it was authorised
in. Its tools were absent from three separate lookups.

**What to do:** nothing further to authorise. Just **start a new chat**. The connector will
attach at session start.

**What it unblocks, in priority order:**
1. The www to apex 301 redirect. This is the actual cause of the cookie dialog reappearing,
   and it also consolidates SEO across two hostnames that currently both serve 200.
2. A full optimisation pass: caching rules, Early Hints, Brotli, HTTP/3, image resizing.
3. Bot management and WAF rules to stop the item bank being harvested.
4. Reading Worker analytics and deploy history.

If for any reason the connector still does not appear in a fresh session, the redirect is a
two minute job in the dashboard: **Rules → Redirect Rules → Create**, matching
`hostname equals www.startfromnowhere.com`, action **Dynamic redirect**, expression
`concat("https://startfromnowhere.com", http.request.uri.path)`, status **301**, preserve
query string on.

### 2. Google Search Console, through Supermetrics

**Status:** Supermetrics is connected, but **every Google source reads NOT_AUTHENTICATED**.
The only sources authorised are ones that need no auth at all: Google Trends, Apple Public
Data, Facebook Public Data, Pinterest, Data Blending, Custom Data Import.

**What to do:** in Supermetrics, connect source **`GW` (Google Search Console)** using the
Google account that owns the startfromnowhere.com property. Worth also connecting **`GAWA`
(Google Analytics)** and **`PSI` (PageSpeed Insights)** while you are there.

**Why it matters:** without it, every SEO question needs you to export a CSV by hand. With
it, the weekly agent reads impressions, queries, positions and crawl errors itself.

### 3. The weekly Routine's connectors

**Status:** Routine `trig_019AgLUsR7KEdTqf5hAG29NB` ("Start From Nowhere weekly audit and
improve") exists and is enabled, firing Mondays at 09:00 UTC, first run 2026-09-28. But the
creation call returned a warning: **it stores no MCP connectors**, so the sessions it fires
will have no Supabase and no GitHub. That breaks its live-signal step and its PR step.

**What to do:** go to **claude.ai → Routines**, open that Routine, and attach the connectors
(Supabase, GitHub, Cloudflare at minimum). If the UI does not allow editing connectors on an
existing Routine, delete it and recreate it from the Routines UI, where the grants attach
automatically. The full prompt text is in `HANDOFF.md` so nothing is lost.

## Not tested, and not needed

**Egnyte** and **Shopify** identity probes were blocked by the session's safety classifier,
which reads identity lookups as credential probing. Neither is relevant to this project (file
storage and e-commerce), so this is not worth resolving unless you have a use for them.

**Adobe** was not tested. Potentially useful later for report and document generation.

---

## How to authorise anything

claude.ai → **Settings → Connectors**. Then **start a new chat**, because of the
attach-at-session-start rule at the top of this file.

## What no connector can give me

There is no screen sharing, remote desktop or computer control in the Claude Code session
toolset. Claude does have screen sharing in other products, but not here. Anything requiring
a GUI (the Apple Developer portal, App Store Connect, a Mac running Xcode) has to be you.

---

## Local tooling, fixed by a session start hook

Separate from connectors, but it bit us the same way: a capability that looked present
and was not.

`.claude/hooks/session-start.sh` now runs at the start of every remote session and
installs what a fresh container lacks. **This only takes effect once it is merged to
`main`.**

What it fixes:

- **Playwright.** `node_modules` is gitignored and the container is rebuilt from a clean
  clone, so all four browser smoke suites (`smoke_items`, `smoke_consent`, `smoke_billing`,
  `smoke_offline`) failed on a fresh session with "Cannot find module 'playwright'". The
  browser itself is preinstalled, so only the package is fetched.
- **LibreOffice Writer.** The image ships `libreoffice-core` and `libreoffice-common` with
  no Writer module. This fails confusingly: `soffice` exists, reports version 24.2.7.2, and
  then refuses every document with "source file could not be loaded", including a plain
  `.txt`, because text to PDF also goes through Writer. This is why a Word document could
  be built and validated on 2026-09-21 but not rendered and inspected.
- **poppler-utils and pandoc**, for turning a PDF into images to look at and for reading a
  `.docx` back as text.
- **The python modules the docx skill imports**: defusedxml, lxml, python-docx, openpyxl.
  Without defusedxml its `validate.py` cannot run at all.
- **`CHROMIUM_PATH`, `PLAYWRIGHT_BROWSERS_PATH` and `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD`**
  exported through `CLAUDE_ENV_FILE`, so the smoke suites run exactly as CLAUDE.md writes
  them instead of needing a wrapper each time.

Verified: runs clean twice, writes its env lines once rather than stacking them, exits
silently outside a remote session, and reinstalls a module after it was deliberately
uninstalled. Engine tests, the build and `smoke_consent` all pass using only the
environment the hook exports.
