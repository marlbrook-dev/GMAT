# Growth playbook (Start From Nowhere)

Two engines: inbound (SEO, The Study Room) and outbound (partnerships tracked in the Admin > Partners CRM). Every outbound conversation gets a CRM row with a stage and a next action; nothing lives in inbox memory.

## Outbound channels, in priority order

| Channel | Play | Revenue model | CRM type |
|---|---|---|---|
| Independent GMAT tutors | Offer the trainer as their homework layer; they see student analytics, we get their students | Rev share on referred subscriptions | tutor |
| MBA clubs and consulting clubs at universities | Free premium for club members for a semester; club promotes to members | Conversion after graduation window | community |
| Admissions consultants | Same homework-layer pitch as tutors; they care about score outcomes | Rev share or flat referral fee | partner |
| Study-abroad and test-prep agencies | White-label or bundled seats | Seat licensing | partner |
| Affiliate/deal sites and newsletters | Standard affiliate links once Stripe is live | Affiliate percentage | affiliate |
| Corporate L&D / EMBA feeder programs | Employer-paid seats for GMAT-bound employees | Seat licensing | school |

## Rules for outreach
- Personalized, short, one clear ask. No mass spam; CAN-SPAM applies to cold email (real from-address, working unsubscribe, physical address once we have one).
- Never claim results we cannot back. The honest pitch is the product: free first round, per-skill ratings, spaced review.
- Log every touch in the CRM the moment it happens; set the next action before closing the tab.

## Inbound (already built, keep feeding)
- The Study Room: publish steadily against `design/guidelines/seo-content.md` pillars; refresh score posts yearly; pursue reader success stories, they convert best.
- Google Search Console after domain connect; watch which queries earn impressions and write the missing pieces.
- Every article ends with the free-round CTA; the trainer itself is the top of the funnel (no account needed to start).

## Not yet, revisit later
Paid ads (needs pricing + conversion data first), YouTube worked-problem shorts (time cost), podcast guesting (needs a story arc: real user score gains).

## Answer engine optimization (GEO)
AI assistants (ChatGPT, Claude, Perplexity, Google AI Overviews) increasingly answer "best GMAT prep" and "good GMAT score" questions directly, citing third-party mentions and clean, sourced reference pages rather than brand homepages.
- On-site (done): robots.txt welcomes AI crawlers, /llms.txt gives them a structured summary, every article carries FAQ and Article structured data, sourced tables, and a quotable first paragraph.
- Off-site (the real lever): brand mentions in credible surfaces the models cite: contributed pieces or quotes in approved outlets, tutor and consultant partner pages, university club resource lists. Track each pursuit in the Partners CRM.
- Measure quarterly by hand until tooling matures: ask the major assistants the top 10 queries from seo-content.md pillars and log whether we appear, what they cite, and what they get wrong.

## Search: What Google Is Already Showing Us

Written September 26, 2026 from the owner's Search Console export for August 18 to
September 24, 2026. Rerun it on any later export with `python3 src/gsc_report.py <file>`;
the raw export is the owner's and is never committed, because this repository is public.

| Measure | Value |
|---|---|
| Impressions | 23,937 |
| Clicks | 12 |
| Click through rate | 0.05 percent |
| Daily impressions, September 1 to 7 | 431 to 781 |
| Daily impressions, September 21 to 24 | 1,412 to 1,699 |

The site is indexed and shown, almost entirely on pages three to six. Clicks are near zero
because position is, not because snippets are bad: Advanced Web Ranking's July 2026 study
of US desktop results puts position 20 at 0.27 percent and position 3 at 3.89 percent
(advancedwebranking.com/seo/organic-ctr, retrieved September 26, 2026).

**Where the impressions go.** `/schools/` pages take 13,907 (58 percent) at an average
position of 34; `/colleges/` 5,377 at 42; the blog 2,615 at 54; exam guides 1,959 at 54.

**What people were asking**, by impressions:

| Intent | Impressions | Average position |
|---|---|---|
| School or college name alone | 3,370 | 47 |
| Acceptance rate | 2,204 | 49 |
| Cost or tuition | 1,181 | 48 |
| Ranking | 744 | 34 |
| Class profile | 720 | 20 |
| Study plan | 428 | 48 |
| Exam format or length | 398 | 55 |
| Average GMAT or GRE | 386 | 36 |
| GMAT vs GRE | 130 | 76 |

Three conclusions, each acted on in the pull request that added this section:

1. **Class profile is where we already compete** (average position 20, the best of any
   intent), so the school pages now answer class profile questions in sentences as well as
   tables: GMAT, GRE, GPA, work experience, class size, each with the statistic the school
   actually published (average or median) and the class it describes.
2. **Acceptance rate is the biggest intent and the one we can least answer**: the library
   holds a verified rate for only 16 of 91 programs, 8 from the schools' own sites and 8 from
   publishers. The pages show a dash rather than an estimate, and say the rate has not been
   verified rather than that the school does not publish one (INC-0118). For
   colleges, where the federal Scorecard does carry it, acceptance rate queries are 375 of
   the 763 impressions on queries naming a college, at an average position of 21, so it now
   leads every college snippet.
3. **Two withdrawn pages were still ranking** (the Executive Assessment guide at position
   9.6) into a 404 that is the whole GMAT trainer. They now redirect to the exams hub, and
   the report tool flags any URL with impressions that the build no longer produces.

What moves position from 34 to page one is not on the page. Google's own starter guide says
it finds pages "primarily" through links from other sites and that changes can take
"several months" (developers.google.com/search/docs/fundamentals/seo-starter-guide). The
outbound channels at the top of this file are the ranking work; the page work only makes
sure that when a searcher does arrive, the answer they came for is the first thing they read.

## What Brings People Back: Research and What We Built From It

Written September 26, 2026. Search brings a visitor once; the products that grow on repeat
visits give them a reason to return tomorrow. This is what the best of them do, read from
their own pages the same day, and what it means here. Where a source could not be read it
is named, not substituted.

### What the evidence says

| Mechanic | Who runs it | Evidence |
|---|---|---|
| One shared puzzle a day, the same for everyone | NYT Wordle; Chess.com daily puzzle; College Board's own SAT question of the day | satsuite.collegeboard.org/help-center/how-does-question-day-work; support.chess.com/en/articles/8708990-how-does-the-daily-puzzle-work |
| A result you can share without spoiling it | Wordle's grid, adopted from a player's invention; Chess.com's share card | techcrunch.com/2022/01/12/josh-wardle-interview-wordle |
| Streaks that protect the habit, with freezes | Duolingo: letting learners hold two freezes lifted daily actives 0.38 percent; learners who reach a 7 day streak are 3.6 times likelier to finish a course | blog.duolingo.com/how-duolingo-streak-builds-habit |
| A streak that survives a wrong answer | Chess.com keeps the daily streak at zero hearts; Brilliant counts activity, not accuracy | support.chess.com (above); brilliant.org/help/features/what-is-a-streak |
| Broken streaks lower engagement, repairable ones less so | Silverman and Barasch, Journal of Consumer Research | academic.oup.com/jcr/article-abstract/49/6/1095/6623414 |
| Better reminder wording alone moves retention | Duolingo's bandit-chosen reminders: 0.5 percent more daily actives, 2.0 percent better new-user day 7 retention | research.duolingo.com/papers/yancey.kdd20.pdf |
| Personal bests, no leaderboard | Lichess Puzzle Storm keeps bests by day; its FAQ: "Where there is a leaderboard, there is cheating." | lichess.org/page/storm |
| Due-review queue as the daily session | Anki's spaced intervals mean some cards come due every day | docs.ankiweb.net/background.html |

Page families that earn search traffic for comparable sites, all loaded on the same day:
per-college admissions pages (PrepScholar, CollegeVine), per-school deadline pages under a
hub (Clear Admit), score and superscore calculators (ACT's own superscore FAQ hosts one),
dated daily question pages (Chess.com), and study plans by duration (Magoosh).

**Could not be read**, and nothing here relies on them: nytimes.com and nytco.com, Duolingo's
help center (renders empty), LeetCode, Quizlet and Khan Academy support pages (403), GMAT
Club (403), kaptest.com (403), Niche (403), US News (503), Shiksha (403), and OpenAI's help
pages on ChatGPT search (403).

### What was built from it

- **Daily Questions at /daily/**: one hand-written question per exam per day, fixed in advance
  in data/daily/schedule.json so it is the same for everyone and never changes afterwards.
  The trainer's Question of the Day now serves the same question. Every past day stays online
  as a dated page with its answer and explanation, and each exam has an RSS feed.
- **A streak that counts showing up.** The old one reset to zero on a wrong answer, which
  punished exactly the people who came back. It now counts days answered, keeps accuracy as a
  separate best run, and earns a freeze every seven days (two at most, never sold). It lives
  only in the visitor's browser and is shared between the public pages and the trainer.
- **A spoiler-free share**: exam, date, solved or missed, time and streak; never the question
  and never the answer, which a test checks.
- **Measured without identifying anyone**: each answer on /daily/ posts the same unlinkable row
  the trainer already sends (item, option, right or wrong, seconds; no account, session,
  device or address). Answers per day on /daily/ are the number to watch:
  `select date(ts), count(*) from item_events where mode = 'daily' group by 1 order by 1`.

### Next, in the order the evidence ranks them

1. **An opt-in reminder email carrying the question.** Kaplan and ACT both deliver a daily
   question to an inbox or account (kaplanquizzes.com; act.org free test prep). This needs an
   owner decision on a sending provider, a consented list, a one-click unsubscribe, and a
   privacy.html update before anything is collected.
2. **Due-today flashcards on the dashboard and the daily page**, using the decks already
   shipped, so there is a second reason to return that is about memory, not novelty.
3. **Score calculators built only from published rules**: the ACT Composite (the average of
   English, Mathematics and Reading, which ACT publishes) and superscores. Never a percentile
   or a conversion table we cannot source.
4. **Per-school MBA deadline pages**, which Clear Admit runs as a hub. Blocked on data: only
   one school file carries a deadline, and each must come from the school's own page.
5. **An ICS export of the application checklist**, so the dated tasks on /apply/ land in a
   calendar that reminds the applicant instead of us.

Left out on purpose: weekly leagues and percentile ranks (they rank people against each
other), prize drawings (luck), and self-reported decision feeds (unsourced figures on the page).

## Revenue: What the Numbers Actually Support

Written September 15, 2026, against real analytics rather than ambition. Every
figure in this section is from `site_events` or a primary source, and the
arithmetic is shown so it can be redone when the traffic changes.

### The Traffic Reality

First 28 days of measured traffic (August 19 to September 15, 2026):

| Measure | Value |
|---|---|
| Pageviews | 366 |
| Sessions | 124 |
| Sessions from the United States | 95 (77 percent) |
| Sessions from India | 5 |
| Sessions from all of Asia combined | 16 |
| Sessions from Hong Kong | 0 |

Two things in there are worth more than the totals. Organic search is already
landing non-US readers on `/schools/` specifically, from Google, in Japan,
Korea, Poland, Israel and Singapore. And ChatGPT is a real referrer, sending
visitors from India, Germany and Vietnam. The answer-engine work in this
playbook is producing traffic; the volume is just small.

### Why Display Advertising Earns About Five Dollars a Month Here

At 366 pageviews in 28 days, call it 400 a month. Three ad units per page is
1,200 impressions. Education content in the United States can reach a $15 RPM
on a premium network and a small site on an open network realistically sees
$2 to $6. So:

- Optimistic: 1,200 impressions at $15 RPM = **$18 a month**
- Realistic: 1,200 impressions at $4 RPM = **$4.80 a month**

That is the whole opportunity at today's traffic, and it is not a forecast that
improves with effort on the ad side. It improves only with traffic.

The premium networks that pay the high RPM will not take us yet in any case.
Mediavine's lowest tier, Journey, requires 1,000 monthly sessions; we have
about 130. (Source: Mediavine's programs page, retrieved September 15, 2026.)
Raptive's published minimum is higher still, but note that their eligibility
page returned HTTP 403 to us, so the specific number is unverified here and
should be checked before anyone quotes it.

### The Three Costs Ads Carry Here, Which Are Not Small

1. **Page speed, which is the growth engine.** Every visitor outside the United
   States arrived through organic search or an AI assistant. Third-party ad
   scripts are the single most reliable way to damage Core Web Vitals. Trading
   measurable search performance for $5 a month is a bad trade at any traffic
   level, and a catastrophic one at this level.

2. **The privacy posture, which is the product's differentiator.** The site runs
   a first-party beacon with no third-party trackers, and `privacy.html` says
   so. An ad network is a third-party tracker by definition. Running one means
   rewriting those disclosures, adding a consent management platform for EU
   visitors, and giving up a claim that currently distinguishes us from every
   competitor in this category.

3. **Indian law makes it unlawful on the SAT side.** India's Digital Personal
   Data Protection Act, 2023 defines a child as anyone under eighteen
   (section 2(f)), requires verifiable parental consent before processing a
   child's personal data (section 9(1)), and states plainly at section 9(3)
   that "A Data Fiduciary shall not undertake tracking or behavioural
   monitoring of children or targeted advertising directed at children."
   Breach of the section 9 obligations carries a penalty that "may extend to
   two hundred crore rupees" under the Act's Schedule. The SAT audience is
   overwhelmingly under eighteen. Targeted advertising cannot be served to it
   in India, and an untargeted fallback earns a fraction of an already tiny
   number. (Source: the Act as published by the Ministry of Electronics and
   Information Technology, retrieved September 15, 2026.)

**Recommendation: do not add display advertising now.** Revisit when the site
clears roughly 25,000 monthly pageviews, which is both the point where premium
networks become available and the point where the revenue stops being a
rounding error. The decision is a traffic milestone, not a judgment call, so it
can be automated: watch monthly pageviews in the admin traffic view.

### What Does Make Money at This Stage, In Order

1. **Turn on the subscription that is already built.** Stripe Checkout is
   scaffolded and `PAYMENTS_LIVE` is false. One paying subscriber is worth more
   than a year of display ads at current traffic. This is the highest-value
   revenue action available and it needs the owner's decision, not more code.

2. **Partnerships already in this playbook.** Tutors, admissions consultants,
   university clubs, agencies. Revenue per relationship dwarfs per-impression
   revenue at small scale, and none of it touches the privacy posture.

3. **Affiliate relationships, but only where they are honestly useful.** The
   international audience genuinely needs lenders who do not require a US
   cosigner, and those lenders pay referral fees. Two hard conditions if we
   ever do this: an affiliate relationship may never influence a ranking, a
   score, or an ordering anywhere on the site, and every affiliate link must be
   labeled as one at the point of the link, not in a footer. If either is
   inconvenient in a given deal, decline the deal.

4. **Qualified applicant leads to schools**, which is the large money in this
   vertical. It is also the one that most easily becomes something we would not
   want to explain: it only works with explicit, specific, revocable opt-in from
   the applicant, naming the schools their information goes to. Anything less is
   selling readers. Worth building properly, later, or not at all.

### The India Question, Answered Directly

India is the second-largest source of traffic and the largest source of GMAT
test takers outside the United States, so building for Indian applicants is
plainly right. But "gather their data so we can advertise to them" is the one
version of it that does not work, for the three reasons above and one more: it
would be the first thing on this site that we could not explain to the reader
it was done to.

What works instead, and is already half built:

- **The international guide and the checklist are the India product.** The CIP
  code question, OPT arithmetic, H-1B caps, and funding without a US cosigner
  are the questions an Indian applicant actually has, and almost nobody answers
  them with sources attached.
- **Ask for data the reader gets something back for.** Target exam, target
  score, target schools, application round, country. The checklist and the
  trainer need these to function, so the exchange is visible and fair. This is
  first-party, declared, and useful, which is exactly the standing rule in
  CLAUDE.md: demographics optional, self-reported, on the Account page only,
  never inferred, bought, or appended.
- **Serve the notice in the right language.** The DPDP Act section 5(3) gives a
  data principal the right to access the notice "in English or any language
  specified in the Eighth Schedule to the Constitution." If we take Indian
  users seriously enough to build for them, the privacy notice is the first
  thing to translate, ahead of the marketing copy. See I18N.md.
- **Price for the market.** Purchasing power parity pricing does more for
  conversion in India than any amount of targeting, and it is a pricing
  decision, not a tracking one.

### Revisit Triggers

Re-read this section when any of these becomes true, and not before:

- Monthly pageviews clear 25,000 (reconsider display advertising).
- Monthly sessions clear 1,000 (Mediavine's Journey tier becomes available).
- A non-English-speaking country produces real Search Console impressions
  (trigger for I18N.md Stage 1).
- `PAYMENTS_LIVE` flips to true (subscription revenue becomes measurable, which
  changes the comparison every option above is measured against).
