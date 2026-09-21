# The Stack, Priced, and What It Would Cost in Open Source

The whole platform runs for roughly the price of a couple of lunches a month. That is not
a boast, it is the design constraint that produced most of the interesting decisions in
this book, and it is reproducible.

## What is actually running

| Layer | Choice | Why this one | Monthly at this scale |
| --- | --- | --- | --- |
| Hosting and CDN | Cloudflare Workers with static assets | Global edge, generous free tier, and a real runtime in front of the files when you need one | $0 to $5 |
| Domain | Registrar of choice at cost | Nothing clever here | about $1 amortised |
| Database, auth, storage | Supabase (managed Postgres) | Row Level Security means the database enforces authorisation, not the app | $0 to $25 |
| Serverless functions | Supabase Edge Functions (Deno) | Same project, same secrets store, no second vendor | included |
| Payments | Stripe Checkout, Apple In-App Purchase | Checkout removes PCI scope entirely; Apple is mandatory if you ship an iOS app | percentage of revenue |
| Email | Transactional provider of choice | Deliberately last. Do not build this before you have users | $0 at low volume |
| Source and CI | GitHub with Actions | The deploy hook and the test runner live in the same place as the code | $0 |
| Error and product telemetry | Written in house, about 200 lines | Covered below; this is the surprising one | $0 |
| Analytics | First-party beacon, written in house | Covered below | $0 |
| Charts | Written in house, one file | Covered below | $0 |

Total fixed cost at the scale this platform runs: under thirty dollars a month, most of
which is the database.

## The three things not to buy

These are the decisions that saved the most money and, more importantly, the most
complexity. Each replaced a product that would have been reasonable to buy.

**Analytics.** A first-party beacon is a `fetch` on page load carrying path, referrer,
UTM parameters, a session id from `sessionStorage`, device class and time on page, into
one table. Country and a salted address hash are added by a database trigger so the raw
address is never stored. That is a few dozen lines. What you get that you cannot buy:
the data is in your own database next to your users, so a question like "which landing
pages precede a subscription" is a join rather than an integration project. What you give
up: nothing an ad blocker was not already taking from the paid product.

**Error monitoring.** A global `error` and `unhandledrejection` handler posting to an
insert-only table, with a clustering view and a human triage queue. The clustering matters
more than the capture: raw errors are noise, and the value is in a human marking each
cluster real, fixed, will not fix, or noise, so the queue gets quieter as it learns rather
than louder. Nothing in it edits code, and that is deliberate.

**Charts.** A charting library is two hundred kilobytes and a second thing to pin in your
Content Security Policy. Five chart forms plus a stat tile, built as inline SVG from
numbers, is about six hundred lines and smaller than the smallest library's minified core.
The chapter on the interface explains why the colours in it are computed rather than
chosen.

The rule behind all three: **buy the thing that would be dangerous to get wrong, build the
thing that is mostly a shape.** Payments are dangerous. Authentication is dangerous. A bar
chart is a shape.

## The open-source equivalent of every paid piece

If the managed services are unavailable, too expensive, or politically impossible, here is
the substitution, and honestly what it costs you.

| Managed | Open source | What changes |
| --- | --- | --- |
| Cloudflare Workers | Caddy or nginx on a small VPS; Nixpacks or Dokku for deploys | You now own TLS renewal, log rotation and the box. Budget half a day to set up and an hour a month forever |
| Supabase | Postgres plus PostgREST plus GoTrue, or the self-hosted Supabase compose file | You get the same API surface. You also get backups, upgrades and connection pooling as your job. This is the biggest jump in operational load of anything in this table |
| Supabase Edge Functions | Deno Deploy, or a plain Node or Deno process behind the reverse proxy | Straightforward. The awkward part is secrets, which you will end up managing with something like SOPS or a mounted env file |
| Stripe Checkout | There is no real substitute, and you should not want one | Self-hosting payments means PCI scope. Do not |
| GitHub Actions | Forgejo Actions, Woodpecker, or Drone | Fine. Slower to set up, one fewer vendor |
| Managed Postgres backups | pgBackRest or WAL-G to object storage | Works well and is genuinely worth learning even on a managed service, because it is also your migration path off it |
| Supabase Auth | Keycloak, Authentik, Ory Kratos | All three are more capable and considerably more work. Keycloak in particular is a serious piece of infrastructure |
| Cloudflare Web Analytics | Plausible, Umami, Matomo, all self-hostable | Umami is the lightest. But see the point above: once you have a first-party beacon into your own database, a second analytics product is mostly duplication |
| Playwright | Already open source | No change |
| Anything for charts | ECharts, Chart.js, Observable Plot | All good. Weigh the bundle against the six hundred lines |
| Anything for PDF | Headless Chromium print-to-PDF, WeasyPrint, Typst | Chromium is already on the machine if you run browser tests. That is how this document is produced |

**The honest summary of that table:** the only irreplaceable paid component is the payment
processor. Everything else is a convenience purchase, and the convenience is real but
bounded. The thing you are actually buying from a managed database is not Postgres; it is
somebody else being on call for it.

## What the architecture buys you

Two structural choices shaped everything else, and both are worth copying.

**Static pages, built ahead of time, with no runtime framework.** Every page on the site
is a self-contained HTML file with inline CSS and inline JavaScript, generated by a Python
build. There is no server rendering, no hydration and no client-side router. The
consequences compound: pages are fast because there is nothing to boot; the whole site can
be served from a CDN for nothing; there is no dependency tree to keep patched; and the
security surface of a page is what you can read in that page. The cost is that anything
dynamic has to be deliberate, which turns out to be a feature.

**The database enforces authorisation, not the application.** Row Level Security on every
table, and every privileged read behind a `SECURITY DEFINER` function that checks an admin
table. The app cannot grant itself anything, because the app is a browser, and a browser
is not trusted. This is what makes it safe to ship a site with no backend of your own.

Both decisions have the same shape: **push the guarantee down to the layer that cannot be
bypassed.** A rule enforced in JavaScript is a suggestion.
