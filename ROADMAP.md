# Start From Nowhere: build roadmap

Updated September 14, 2026. Owner: Hunter Roberts. Builder: Claude sessions. This file is the working schedule; each week's block ships as one or more merged PRs. Dates are targets, not promises; anything user-facing ships only after the browser test suite passes.

## Comparative advantage (the why-us, revisited each cycle)

1. Game-grade engagement on top of real per-skill analytics. Competitors have one or the other, not both.
2. Radical honesty: original items, sourced statistics, no fabricated testimonials or efficacy claims, transparent methodology everywhere. Trust is the moat an institutional audience actually pays for.
9. The rankings-to-study loop: pick target schools, get a study plan calibrated to their published numbers, watch fit improve as ratings rise. No competitor closes this loop.
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
- [x] Blog: 4 new posts including 2 rankings-adjacent (how to read class profiles; GMAT scores for top programs, citing our own library)

## Week of Sep 9

- [x] Executive Assessment mode, first slice: EA-format mock (40 questions, three 30-minute sections, honest labeling); score-model deepening still open
- [ ] User-profile fit inputs: GPA, work experience, budget; fit view against school library
- [ ] Beta push: founding-user outreach wave via CRM (tutors, clubs, consultants)

## Week of Sep 16 and beyond

- [x] Undergrad pilot, first half: SAT trainer live at /sat/app/ on a genuinely multi-exam engine, 248 original items across all eight official content domains, two-module mock sections with routing, grid-ins, a 112-card deck and a playbook per domain, site wiring
- [ ] Undergrad pilot, second half: undergrad rankings vertical (one file per college, same source ladder as data/schools/), SAT bank toward GMAT parity, ACT study modes
- [ ] GRE build: new item types (text completion, sentence equivalence, quantitative comparison), GRE bank seed, section timing
- [ ] LSAT build: logical reasoning and reading comprehension banks
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

## Session Log: September 14, 2026 (PR 30)

Shipped the SAT vertical. src/engine.js became a real exam registry: SKILLS and
SECTION_META now resolve from an EXAM_ID the build injects, so one engine and
one UI template serve every exam and progress stays keyed per exam. GMAT
behavior unchanged. Caught and fixed a latent bug in the process: pickQuestions
defaulted its section list to the GMAT sections, which would have returned
nothing for any other exam.

SAT: eight official content domains as tracked skills, 336 original items (188
Reading and Writing across all four domains, each with its own short passage,
and 148 Math of which 31 are student-produced responses), 112 flashcards, a
playbook per domain, and a trainer at /sat/app/. Mock sections run as two
modules with the second routed harder or easier by the first, free answer
changes inside a module, and a report broken out by module and by content
domain against College Board's published question ranges. That depth carries
3.5 non-repeating Reading and Writing sections and 3.4 Math sections, so three
full mocks do not recycle.

One gap found by measuring rather than by a failing test: the bank could not
fill an easier second module. Reading and Writing had 9 items at difficulty 1
to 2 against the 27 a module needs, so a student who struggled through module 1
and routed down was served a module built mostly from level 3 items, failing
exactly the students routing exists to help. 38 items written at difficulty 1
and 2 fixed it, and a test now fails if either section drops below the easy
items one module needs. No 400 to 1600 score is reported anywhere;
sources and the two deliberate departures from official practice are documented
in the Exam Content Sources section of data/DATA.md.

GMAT: bank 420 to 448. Multi-Source Reasoning was the thinnest tracked skill at
15 and is now 31, via four new three-tab sets. Plan / Construct 32 to 38,
Identify Stated Idea 28 to 32 (new RC passage P11).

Cross-exam integrity, found by auditing the built SAT app rather than by a
failing test. The two trainers share an origin and an account, and three paths
crossed between them: Store.load fell back to the legacy gmat_trainer_v1 key on
any exam; targetSchools read the MBA list on both, so the SAT dashboard could
show "Published GMAT"; and profiles.state_blob holds one state per user while
attempts, skill_ratings and review_queue are keyed by (user_id, exam), so the
second app a signed-in student opened would overwrite the first exam's
progress. All three are now guarded client-side, and the Account page states
plainly when cross-device sync for an exam is unavailable and that nothing is
lost. The real fix is supabase/migrations/PROPOSED_exam_states.sql, written and
deliberately not applied: it changes the owner's live project.

Also fixed on the SAT app: the browser tab and meta description read "Adaptive
GMAT Focus trainer", a new profile recorded its exam as GMAT, and Number Crunch
was sold as no-calculator practice when Bluebook gives SAT students Desmos on
every Math question. Site-wide, the shared footer named only GMAC and the terms
page omitted the College Board and ACT marks.

Answer key balance, the worst defect found and the one that would have been
hardest to notice from inside the app. Of 302 SAT multiple-choice items, 225
had their correct answer at position A and 3 at D, so a student could have
scored well above their ability by guessing A and every rating derived from
that would have been inflated. The same measurement on the pre-existing GMAT
bank showed position E holding 27 of 324 non-Data-Sufficiency items against an
even share of 65. Both are fixed: numeric choice sets are sorted ascending the
way both real exams present them, everything else takes a permutation seeded
by the item id, and choice-letter references in the explanations travel with
the text. A before and after snapshot proves on every touched item that no
correct answer changed and that every "Choice B is a comma splice" still names
the option that is a comma splice. Data Sufficiency is untouched by design: its
five choices are a standardized set whose order is part of the format.

Length bias, measured and only partly fixed. On a well-built test the correct
answer is no likelier to be the longest choice than any other. It currently is:
the longest choice is correct on 33 percent of SAT items against 25 by chance,
and on 35 percent of GMAT items against 20. The cause is structural, since on
Rhetorical Synthesis and Command of Evidence the key has to combine two pieces
of information while a distractor states one. 60 distractors across 22 items
were rewritten on the model the real exam follows, which took items over
threshold from 88 to 72 and those two item types from a mean ratio of 1.45 to
1.33, but moved the headline figure by one point because 280 items are
untouched. Queued with the numbers and the technique rather than claimed as
done.

Tooling: test.js runs the whole suite once per exam and adds SAT coverage for
module construction, official domain ordering and mix, routing, whether an
easier module can be filled, and grid-in equivalence. It fails if any answer
position takes more than 1.6 times an even share, and reports length bias every
run with a loose guard, because a tight one would fail on every commit until
that content pass is finished. The build now fails on an em or en dash in any
hand-edited doc or bank, and on any item count quoted in llms.txt or the
EDITORIAL fact sheet that no longer matches the real banks. That guard caught
three drifts during the session.

Blog: two queued SAT posts, on the digital SAT format (September 30) and on
building a study plan from the official domain weights (October 2), plus a
corrected SAT vs ACT post (queued September 26, not yet published) that said
our SAT trainer was in development. A third post on SAT percentiles was
dropped rather than written from memory: see the tooling blocker in the queue.

Site totals at the end of the session: 784 original practice items across two
live trainers, 232 flashcards, 22 playbook entries, and two exams wired through
the landing page, the shared header, the exam hub and the pricing matrix.

Next session queue, in order:
1. SAT bank onward from 336: coverage is even across the eight domains (27 to
   34 items each) and grid-ins are 21 percent of Math against roughly a
   quarter on the real test. The next increment should take the bank past
   three non-repeating sections per section and raise grid-ins the rest of the
   way.
2. Length bias in both banks, measured but only partly fixed. On a well-built
   test the correct answer is no likelier to be the longest choice than any
   other. It currently is: the longest choice is correct on 34 percent of SAT
   items against 25 by chance, and on 35 percent of GMAT items against 20,
   while the shortest choice is correct on only 9 percent of GMAT items. A
   student who always picked the longest answer would beat guessing. The cause
   is structural rather than careless: on Rhetorical Synthesis and Command of
   Evidence the correct choice has to combine two pieces of information while
   a distractor states one, so it runs longer unless the distractors are
   written to match. 18 distractors on the worst items were rewritten to the
   same specificity, which improved those items and made their traps harder,
   but barely moved the aggregate because roughly 88 SAT items and a similar
   number of GMAT items sit above the threshold. Fixing it properly is a
   content pass over those items, rewriting distractors to match the correct
   answer in length and specificity without creating a second defensible
   answer. test.js reports the figure every run and fails only past 1.8 times
   chance, so the number is visible without failing on every commit.
   Progress so far: 60 distractors rewritten across 22 items, which took the
   items over threshold from 88 to 72, the bank mean ratio from 1.09 to 1.07,
   and the Rhetorical Synthesis and Command of Evidence mean from 1.45 to 1.33.
   The headline figure moved only from 34 to 33 percent, because it is binary
   and 280 items are untouched. The technique that works is on show in SR126,
   SR091 and SR161: give each distractor two notes rather than one, aimed at
   the wrong goal, and let at least one run longer than the key. Repeating that
   across the remaining items is the job; the GMAT bank needs the same.
3. Undergrad rankings vertical, to close the rankings-to-study loop for SAT
   students the way data/schools/ does for MBA candidates. Needs an owner
   decision on scope (how many colleges, which published figures) before the
   source ladder can be written.
4. Figma iteration 2 implementation (owner's Make credits return 8/31; the
   iteration-2 prompt and guidelines are already in the Make file).
5. School data: re-verify 5 bot-blocked expansion candidates (Arizona Eller,
   JHU Carey, Baruch Zicklin, Oklahoma State, Iowa State) and the blocked
   domains (Columbia, Michigan Ross, Georgia Terry, Case Western); protocol
   and merge tool live in data/research/.
6. Supabase migrations waiting on the owner, all written and none applied:
   supabase/migrations/PROPOSED_exam_states.sql (per-exam state, which restores
   cross-device sync for a student's second exam, plus an exam column on
   sessions), and the forum decisions already queued: pinned threads, tags,
   post votes, view counts.
7. Engine tuning question for the owner, with a reproduction in hand. The
   weakest-first weighting in pickQuestions works as designed for an average
   student: after 120 questions every GMAT skill has 7 to 18 attempts. For a
   student answering about 20 percent correctly it concentrates hard, and one
   skill can be left essentially unsampled: in a simulated run q_rrp got 29
   attempts and di_gt 31 while di_tpa got 2, so the dashboard can tell that
   student nothing about Two-Part Analysis. The diagnostic pass exits once
   half the skills have 3 attempts, and grouped item types (TPA, MSR) are the
   ones that lose out. Worth deciding whether to guarantee a floor per skill
   before targeting takes over; not changed here because it is tuned product
   behavior, not a defect.
8. EA score-model deepening; user-profile fit inputs (GPA, work exp, budget).
9. Tooling blocker, worth fixing before any SAT score-data content. College
   Board publishes mean scores and percentile tables only in PDF (the Total
   Group Annual Report and Understanding SAT Scores). Both download fine, but
   this container has no poppler-utils and its python cryptography module is
   broken, so pypdf and pdfplumber both fail and the tables resist raw stream
   extraction because they use subset font encodings. Anything needing SAT
   percentiles, mean scores, or benchmark figures is blocked until a PDF text
   extractor is available in the build environment. Nothing was written from
   memory in the meantime; the two SAT posts queued use only facts verified
   from HTML sources.
10. Blog: SAT posts for the drip, written to EDITORIAL rules (the digital
   format, what module routing means for a student, how to read a score
   report by content domain).
