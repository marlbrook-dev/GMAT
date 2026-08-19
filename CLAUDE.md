# Start From Nowhere: standing rules for every session

Owner: Hunter Roberts (admin emails: marlbrookgroup@gmail.com primary, hroberts@winthropcapital.com backup). Live site: startfromnowhere.com (Cloudflare Worker "gmat", deploys from main). Read ROADMAP.md for the current build schedule and src/blog/EDITORIAL.md for content rules before writing anything.

## Typography and layout (essential, per the owner: "the little details matter")

- Headers are Title Case everywhere: page titles, section headings (h1/h2/h3), nav labels, card titles, and buttons that name a destination or action ("Create Account", "Download CSV"). Small words (a, an, the, of, and, or, to, for, by, in, on, at, vs) stay lowercase unless first or last. Body copy, descriptions, and table cells stay sentence case.
- Headers must line up: consistent section padding, aligned baselines across cards in the same row, equal gaps in grids. No section may introduce its own one-off spacing values; use the shared spacing scale already in each page's CSS.
- No excess white space: sections are compact; nothing renders as a mostly-empty viewport.
- Kerning and font discipline: headings use the serif display stack, UI labels use the display sans, body uses the body sans, numbers in tables use the mono stack. Never introduce new fonts.
- The wordmark and logo are monochrome navy (#122B4E) and identical on every page; the wordmark always links to /.
- The site header (Exam Prep / Lists / Resources + Sign In + Create Account) is identical across landing, exams, schools, pricing, and blog pages. The trainer app keeps its own tab header, hidden during active sessions and games (focus mode).

## House style (hard rules, build fails on some of these)

- NO em dashes and NO en dashes anywhere: pages, posts, code strings, data files, commit messages.
- GMAT Focus (205 to 805) and Classic (200 to 800) are never converted or mixed; compare by percentile only (Classic 700 = Focus 655, 90.5th percentile, GMAC concordance).
- Never state a school statistic, price, or exam fact from memory. Every published figure carries source, year, and URL; unverifiable = null/dash, never a guess. Banned sources: GMAT Club, Quora, Wikipedia, GyanDhan, Pagalguy, forums, coaching-site blogs.
- Never fabricate product stats, user counts, testimonials, or efficacy claims. Personal bests, not leaderboards; accuracy-only game scoring, nothing luck-based.
- Blog: pen-name bylines with no invented credentials; never backdate; posts publish by date via the drip (one post every 2 days; daily publish cron).

## Engineering workflow

- Develop on the designated claude/* branch; ship via PR to main, squash merge; main deploys the live site via Cloudflare Workers Builds.
- python3 src/build.py builds everything (app, landing, rankings, exams, pricing) and node-parses every inline script; cd src && node test.js runs engine tests; validate in headless Chromium (executablePath /opt/pw-browsers/chromium-*/chrome-linux/chrome) before shipping.
- Generated outputs are gitignored (/app/, /blog/, /schools/, /exams/, /pricing/, index.html, 404.html, sitemap.xml); sources of truth live in src/ and data/.
- JS-in-string onclick handlers must escape single quotes (this class of bug once took down the whole app; the build guard catches it).
- Supabase project: ftsqwbzhkzuudogkvoqa. Payments: Stripe Checkout only, PAYMENTS_LIVE=false until the owner flips it.
