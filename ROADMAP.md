# Start From Nowhere: build roadmap

Updated August 20, 2026. Owner: Hunter Roberts. Builder: Claude sessions. This file is the working schedule; each week's block ships as one or more merged PRs. Dates are targets, not promises; anything user-facing ships only after the browser test suite passes.

## Comparative advantage (the why-us, revisited each cycle)

1. Game-grade engagement on top of real per-skill analytics. Competitors have one or the other, not both.
2. Radical honesty: original items, sourced statistics, no fabricated testimonials or efficacy claims, transparent methodology everywhere. Trust is the moat an institutional audience actually pays for.
3. The rankings-to-study loop: pick target schools, get a study plan calibrated to their published numbers, watch fit improve as ratings rise. No competitor closes this loop.
4. Speed: solo-operator economics with AI-scale content production, so the bank, blog, and features compound weekly.

## Week of Aug 19 (current)

- [x] Games platform: Match, Memory, Blitz, Number crunch, Boss round, Question of the day
- [x] Bank to 300 items, deck to 92 cards
- [x] Landing FAQ + games grid + honest stats strip; PWA groundwork
- [x] /schools/ MBA rankings pilot: top 25 programs, composite rank across US News, FT, Bloomberg, QS, Poets and Quants with documented weights; verified class profile per school (source and year on every figure); filters and sorting; list builder with CSV export and print-ready PDF report; methodology section
- [ ] Search Console verified and sitemap submitted (Hunter)
- [ ] Cloudflare deploy hook created and added as GitHub secret CLOUDFLARE_DEPLOY_HOOK so the 15 queued blog posts drip out (Hunter)

## Week of Aug 26

- [x] Rankings v1.1: school detail pages (one URL per school for SEO), saved-list account sync, PDF report polish
- [x] Target schools wired into the trainer: goal score from published school figures, dashboard messaging, honest fit banding (below / within / above published ranges; never fake probabilities)
- [x] Bank to 360: fill thinnest skills first (di_msr sets, v_pc), plus 2 more RC passages and 2 MSR sets
- [x] Mastery tiers: named levels per skill mapped to rating bands; tier-promotion confirmation rounds
- [x] Weakest-skill one-tap round and Missed-questions round on dashboard

## Week of Sep 2

- [x] Full mock exam: three sections back to back with break, section order choice, full score report
- [x] Community forum (/community/): five boards on Supabase with RLS, anonymous reading, magic-link posting, human moderation; header entry site-wide
- [x] Forum v2: open posting (named or anonymous pseudonyms), 3-step guided composer, DB-side rate limits and screening, moderation queue in Admin
- [x] Admin v2: Users library (per-user record + filters + CSV/JSON/print report), Traffic tab on a first-party beacon, Moderation terminal, optional self-reported demographics on Account
- [x] Pace meter per question type in recaps; error log v2 (reason tags feed a targeted drill)
- [x] Bank to 420; flashcards to 120
- [ ] Blog: 4 new posts including 2 rankings-adjacent (how to read class profiles; GMAT scores for top programs, citing our own library)

## Week of Sep 9

- [x] Executive Assessment mode, first slice: EA-format mock (40 questions, three 30-minute sections, honest labeling); score-model deepening still open
- [ ] User-profile fit inputs: GPA, work experience, budget; fit view against school library
- [ ] Beta push: founding-user outreach wave via CRM (tutors, clubs, consultants)

## Week of Sep 16 and beyond

- [ ] GRE build: new item types (text completion, sentence equivalence, quantitative comparison), GRE bank seed, section timing
- [ ] LSAT build: logical reasoning and reading comprehension banks
- [ ] Undergrad pilot: SAT/ACT study modes plus undergrad rankings vertical
- [ ] Stripe go-live checkpoint: flip PAYMENTS_LIVE once accounts and legal review are done
- [ ] SFN Assist (AI coaching) when the Anthropic API key is added

## Standing cadence

- Blog drip: 1 to 2 posts per week already queued through Nov 5
- Monthly currency review: GMAC format changes, new class profiles, competitor moves, model upgrades
- Weekly: read Admin BI (item flags, hardest skills, funnel) and act on it in the next build

## Session Log: August 20, 2026 (PRs 22 to 28, all merged)

Shipped: full Figma design pass with shared chrome (src/partials.py); school
library rebuilt to 91 schools on official sources with a build-time validator
(data/schools/, data/DATA.md); rankings presentation with Detailed View
toggle; bank 300 to 420 items; The Ladder game; pace meter in mock recaps;
reason-tag targeted drill; sitemap school URLs restored; 4 queued blog posts
(2 rankings-adjacent, SAT vs ACT, LSAT); EDITORIAL.md fact sheet refreshed;
EA-format mock.

Next session queue, in order:
1. Figma iteration 2 implementation (owner's Make credits return 8/31; the
   iteration-2 prompt and guidelines are already in the Make file).
2. School data: re-verify 5 bot-blocked expansion candidates (Arizona Eller,
   JHU Carey, Baruch Zicklin, Oklahoma State, Iowa State) and the blocked
   domains (Columbia, Michigan Ross, Georgia Terry, Case Western); protocol
   and merge tool live in data/research/.
3. Forum DB decisions with owner: pinned threads, tags, post votes, view
   counts (each needs a migration).
4. EA score-model deepening; user-profile fit inputs (GPA, work exp, budget).
5. Bank beyond 420, thinnest skills first (di_msr and v_pc still lowest).
