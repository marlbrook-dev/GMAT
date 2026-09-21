# Connector setup for Start From Nowhere

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
