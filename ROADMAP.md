# Start From Nowhere: build roadmap

Updated September 26, 2026. Owner: Hunter Roberts. Builder: Claude sessions. This file is the working schedule; each week's block ships as one or more merged PRs. Dates are targets, not promises; anything user-facing ships only after the browser test suite passes.

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
- [x] User-profile fit inputs: GPA, work experience, budget; fit view against school library (shipped in PR 64; About You collects the three, and the dashboard fit card puts them beside each target school's published figures with the source on every one)
- [ ] Beta push: founding-user outreach wave via CRM (tutors, clubs, consultants)

## Week of Sep 16 and beyond

- [x] Undergrad pilot, first half: SAT trainer live at /sat/app/ on a genuinely multi-exam engine, 248 original items across all eight official content domains, two-module mock sections with routing, grid-ins, a 112-card deck and a playbook per domain, site wiring
- [ ] Undergrad pilot, second half: SAT bank toward GMAT parity, ACT study modes. The undergrad rankings vertical is done: 1,451 files in data/colleges/, every figure on the federal College Scorecard with source, year and url, validated by src/validate_colleges.py
- [x] GRE build: new item types (text completion, sentence equivalence, quantitative comparison), GRE bank seed, section timing (all three types live; GRE_SECTIONS carries the unequal 12 then 15 module pair and its 18 then 23 and 21 then 26 minute splits)
- [x] LSAT build: logical reasoning and reading comprehension banks, live at /lsat/app/
- [x] ACT build: English, Reading and Science banks plus Mathematics remapped from the SAT schemas, live at /act/app/
- [ ] MCAT build: BLOCKED ON SOURCE ACCESS, not on engineering (see the September 16 note below)
- [ ] Executive Assessment build: BLOCKED ON SOURCE ACCESS, same note
- [x] Stripe go-live: live products, prices ($4.99 Plus / $9.99 Pro) and webhook created; 7-day trial wired; PAYMENTS_LIVE=true
- [ ] Stripe go-live, remaining: owner sets Edge Function secrets, confirms charges are enabled, and gets terms plus a refund and cancellation policy reviewed
- [ ] Decide what grandfathering means for early users, then flip FREE_LIMITS_LIVE
- [ ] Stripe Customer Portal so students can cancel without emailing
- [ ] SFN Assist (AI coaching) when the Anthropic API key is added
- [x] Business intelligence: billing event ledger (Stripe and Apple), admin_business RPC, Business tab on the chart library
- [x] The Build Playbook: a living, exportable guidebook that captures how this platform was built, every defect and misfire hit along the way, and the reusable infrastructure recipe for standing the same stack up again for a different business (scope below)


## Session log, September 26, 2026: search data, daily questions, reading questions

The ask: another pass at the games, the questions and the school rankings, more work on
the algorithm, what the sites with real repeat traffic do, and growth and revenue across the
site. The owner supplied a Search Console export for August 18 to September 24 (23,937
impressions, 12 clicks, school pages at an average position of 34). The raw export is the
owner's analytics and is never committed; `src/gsc_report.py` turns any export into the same
analysis. Everything shipped in PR 96, four commits:

- [x] **School and college pages** say what the data says (INC-0104 to INC-0110): broken
      intro sentences on half the school pages, salaries labelled as medians that were
      averages, 29 official figures footnoted as secondary, withdrawn exam guides still
      ranking into a 404 and now redirected, and a page suite that had been failing on its
      first click. GROWTH.md records the findings.
- [x] **Daily Questions** at `/daily/`: one hand-written question per exam per day, the same
      for everyone, with a dated archive and an RSS feed per exam, a spoiler-free share and a
      streak that counts days answered, with freezes (INC-0111). The research behind it is in
      GROWTH.md, with its sources and the ones that could not be read.
- [x] **Algorithm**: a coverage floor so weakest-first selection cannot starve a skill
      (INC-0112), explained on `/scoring/` and checked per sitting by the review bots.
- [x] **Games**: Survival, accuracy only, no clock; `src/smoke_games.js` plays every game in
      every trainer, which nothing did before. The 3G first-question time is back inside its
      budget (INC-0113).
- [x] **Reading questions** (INC-0114 to INC-0117): inference keys depended on a rule the
      passage never printed, and three schemas could be answered by matching names or topic
      words on 79 to 95 percent of draws. Both are fixed and guarded at build time. Seven new
      passages take GMAT v_inf from 60 to 81 items, v_st from 140 to 189, LSAT stated from 48
      to 72, main idea from 8 to 12 and inference from 24 to 36.
- [x] **Rankings**: Duke, Boston College and NC State moved to the class that entered in fall
      2026 and Maryland's blank tuition filled, all from the schools' own pages.

**What could not be read this session, and nothing was substituted for it.** US News
(the connection is reset), Poets and Quants (a Cloudflare bot check returns 403), Wayback
Machine snapshots (the availability lookup answers, the snapshot itself is reset), and MIT
Sloan's Class of 2028 profile (its numbers are drawn by JavaScript, and the headless browser
rejects the egress proxy's certificate; verification was not switched off). Acceptance rate
is the largest search intent on the school pages; the library holds a verified rate for 16
of 91 programs, 8 from the schools' own sites and 8 from publishers, so the other 75 need a
publisher table this environment cannot reach. The pages now say a rate has not been
verified rather than that the school does not publish one (INC-0118).

**Owner decisions waiting:**

- [ ] Game scoring: CLAUDE.md says accuracy-only, while Boss Round and The Ladder add a
      time bonus and the landing page says scores come from accuracy and speed. Survival is
      accuracy only. Pick one rule and the games and the copy follow it.
- [ ] Acceptance rates: export the US News or Poets and Quants table, or keep the dash.
- [ ] A provider for the daily reminder email, if one is wanted.
- [ ] Bing Webmaster Tools and IndexNow, which only the domain owner can set up.

### Next session queue

- [ ] More reading passages: every reading category is still far under target, and each
      passage adds ten GMAT items, plus ten LSAT items at LSAT length
- [ ] Read the hand-written reading items against the same two checks (the rule is printed;
      no choice is answerable by matching words); they were not part of this pass
- [ ] Refresh the remaining class profiles as schools post their fall 2026 classes; MIT Sloan
      first, once its page can be read
- [ ] `gmat_ds_linear` and `gmat_ds_inequality` return different items when run twice in
      one process; the build is unaffected because it runs each once, but it is worth knowing
      why before anything relies on calling them repeatedly
- [ ] `src/smoke_load.js` stays out of CI because timing on shared runners is noisy, so run
      it by hand after any change to how the banks are split or loaded (INC-0113)

## Session log, September 16, 2026: LSAT and ACT live, MCAT and EA blocked

Shipped LSAT at `/lsat/app/` and ACT at `/act/app/`, taking the site to five live
trainers. Both were built entirely from the test makers' own published materials;
the source tables are in `data/DATA.md`.

**MCAT and the Executive Assessment are not held back by engineering.** The registry,
the template and the build all take a new exam without a fork. They are held back
because their structural facts could not be verified from this environment:

- `students-residents.aamc.org`, which carries every MCAT structure, timing and
  score-scale page, returns a bot challenge with no content. `www.aamc.org` began
  returning the same after a few requests, and `mcatgpa.aamc.org` is refused by the
  egress proxy.
- `www.mba.com`, which carries the Executive Assessment structure pages, returns an
  Imperva challenge stub on every GET.

What is missing, specifically, before either can go live:

- **MCAT**: section question counts and timings, the 118 to 132 and 472 to 528 scale
  as AAMC states it, and the foundational-concept taxonomy. The rows already in
  `data/exams.json` cannot carry this: the `sections` array has no source field at
  all, and `total_time` and `cost_usd` cite Kaplan, which is a coaching-site blog and
  a banned source under CLAUDE.md. Those rows need replacing, not reusing.
- **Executive Assessment**: the mba.com structure page behind the 100 to 200 total,
  the three 0 to 20 section scales, and the 12 / 14 / 14 question split. The existing
  rows do cite mba.com and were verified in an earlier session, so they are usable for
  the guide page; they were not re-verified on this date.

Unblocking is a five-minute job for the owner: open the two pages and paste the text,
or drop the AAMC "What's on the MCAT Exam?" PDF into the repo. Then both exams follow
the same eight-step checklist as LSAT and ACT.

Also fixed while in here, both pre-existing:

- `src/build_banks.py` seeded each category with `abs(hash(exam + skill))`. Python
  randomises string hashing per process, so every build produced a different bank. The
  README's reproducibility promise was false, and the per-section bias figures pinned in
  `test.js` DEBT drifted run to run, which is a flaky test dressed as a ratchet. It now
  uses `zlib.crc32` and three consecutive builds produce identical output.
- `src/app_template.html` forked on `EXAM.id === 'sat'` in seven places, treating
  "not SAT" as "GMAT". The GRE app had therefore been shipping a score card headed
  "Estimated GMAT Focus Range" and telling GRE students to calibrate at mba.com. The
  copy now comes from the registry (`short`, `blurb`, `official`, `crunch`, `crunchLong`,
  `goals`) and the headless check asserts each app names itself.

Closed on September 22, 2026, and it was worse than this note recorded. `data/exams.json` had
no source validator at all, so nothing had ever read a source on it: ten published figures cited
test prep companies, not one. `sat.score_release` was the least of them and was also factually
wrong, claiming scores land in about 13 days when College Board's own page says 2 to 4 weeks.
All ten were re-verified against the test maker's own page and recited to it, or replaced where
the maker does not publish the claim. `src/validate_exams.py` now enforces the policy: an exam
fact must come from the maker's own domain, which is an allowlist rather than a list of banned
sites, because a blocklist only ever refuses the prep companies somebody thought to name. The
MCAT rows the note also flagged are gone; that exam is not in the file. See INC-0082.

The `sections` arrays were sourced in the same pass. Four of the five now carry a
`sections_src` verified against the maker's own structure page and rendered under the table:
College Board and ETS and ACT all publish a table that matches ours figure for figure, and LSAC
publishes four 35-minute sections with no per-section question count, which is why ours are null.

**GMAT is the exception and it is a blocked source, not a missing one.** `www.mba.com` answers
this environment with a 2 character Imperva challenge stub rather than the exam structure page,
so the 21 / 23 / 20 question counts and their 45 minute sections could not be re-verified.
`validate_exams.py` warns on exactly that one exam. The table is not deleted and no substitute
source is used: CLAUDE.md bans going around a blocked official page, and this needs the owner to
open `https://www.mba.com/exams/gmat-exam/about/exam-structure` and paste the structure table, the
same five minute unblock the MCAT and EA note above asks for.

## The Build Playbook (owner's ask, September 21, 2026)

The ask, in the owner's words: document every single bug, error, misfire and step
involved in building this platform, so the process can be recreated for a different
business idea, with the infrastructure for the website, the app, UI and UX, the business
intelligence system, the algorithm work, the loops, and every other part of the system.
It should cover the open-source options available and the best way to get the right
infrastructure in place. It must be a physical deliverable, a PDF or a Word file, and it
must keep evolving as the build does.

**What makes this hard, and the design that answers it.** A handwritten guide rots. It is
accurate the week it is written and quietly wrong a month later, which is worse than
having none, because a wrong playbook is followed. So the playbook is not a document that
someone maintains. It is a document that is BUILT, the same way the site is built, from
sources that are already kept true for other reasons:

- **Chapters** are prose, in `docs/playbook/`, one file per part of the system. This is
  the part a person writes: the judgement, the reasoning, the tradeoffs, the why.
- **The defect ledger** is structured data, in `data/playbook/incidents.jsonl`, one record
  per bug, error or misfire: what broke, how it was found, what the root cause was, what
  the fix was, what now stops it recurring, and what it cost. Every entry cites the commit
  or the PR it was fixed in, so a claim in the playbook can be checked against the
  repository.
- **The evidence** is harvested at build time, never typed: the guard list comes from the
  real test files, the stack inventory from the real config, the schema from the real
  migrations, the module sizes from the real files on disk. A figure in the playbook that
  nobody can regenerate is a figure that will be wrong eventually.
- **The renderer** is `src/build_playbook.py`, which assembles all three into one document
  and produces HTML, PDF and DOCX. It runs in the same build as everything else and fails
  the same way, so the playbook cannot silently fall behind the thing it describes.

**Adaptive, concretely.** Every incident record carries the rule or guard it produced.
That turns the ledger into the input for the next build rather than a museum: the checklist
chapter is generated FROM the ledger, so a new defect automatically becomes a line on the
checklist the next time the document is built. Recurrence is measurable, because an
incident that happens twice is two records pointing at the same guard, and the renderer
counts them.

Deliverables, in order:

- [x] `docs/playbook/` chapter set and `data/playbook/incidents.jsonl` seeded from this
      repository's real history: 17 chapters, 37 incidents reconstructed from the git log,
      the PR record, the session logs in this file, and the standing rules in CLAUDE.md,
      which are themselves a defect ledger written as instructions
- [x] `src/build_playbook.py`: harvest, assemble, render to Markdown, HTML, PDF and Word,
      with a guard that fails when a chapter cites a file or a commit that does not exist,
      when a harvested figure stops resolving, or when the document breaks the house style
      rule it documents
- [x] The infrastructure recipe chapter: the whole stack priced and justified, the
      open-source alternative for each paid piece, and what it actually takes to stand the
      same thing up from an empty repository
- [x] Wire it into `python3 src/build.py` and CI so the deliverable is regenerated on every
      merge rather than on request. `src/smoke_playbook.js` is where it is blocking; the
      site build warns rather than failing, because a stale chapter should not stop a deploy
- [x] The bootstrap pack: `CLAUDE.template.md`, `KICKOFF.md` and a prompt-sized
      `RULES_DIGEST.md` generated from the same ledger, so a new Claude project starts with
      every defect this build hit already prevented. Layered rather than pasted: the rules
      go in the prompt, the book goes in project knowledge
- [ ] Backfill the ledger further: the August sessions are represented by their commit
      messages only, and the incidents recorded from them are thinner than the ones written
      the day they happened
- [x] A per-incident recurrence count, so the analysis chapter can say which lessons were
      learned twice rather than only which guards are named twice. Each record can name the
      earlier incident whose lesson it repeats, with the quote that justifies it, and the
      count flows into three places: an analysis section, the checklist (repeated rules lead
      their area and say how many times they cost), and the rules digest, which now opens
      with them. It is an explicit claim rather than a computed similarity on purpose:
      trigram overlap across the 84 lessons finds zero pairs, because they are written in
      genuinely different words, and tuning a score down until it reports something would be
      manufacturing a signal. Nine links across seven incidents so far, and the largest
      family runs to six: a correction applied to the instances in hand rather than to the
      pattern, which is this ledger's most expensive habit

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

## Session log, September 15, 2026: international admissions, i18n, revenue

The ask was seven parts: advance the rankings, confirm the blog drip, add
international admissions content, add an application checklist, answer the
translation question, build for Indian applicants, and work out ad revenue.

**First, a premise correction.** The brief said exposure was heavy in Asia,
specifically Japan, India, China and Hong Kong. The analytics do not support
that. Over the first 28 measured days (August 19 to September 15) `site_events`
holds 366 pageviews across 124 sessions: 95 sessions from the United States,
5 from India, 3 Japan, 2 Korea, 2 China, 1 Vietnam, 1 Singapore, 2 Mongolia,
and zero from Hong Kong. Two of the China hits are referrer spam. All of Asia
is 16 sessions of 124.

What is true, and more useful than the premise: the international traffic that
does exist lands disproportionately on `/schools/`, almost all from organic
Google search (Japan, Korea, Poland, Israel, Singapore), and ChatGPT is a real
referrer sending visitors from India, Germany and Vietnam. So the international
work was done, but aimed at the page the data actually points to rather than at
an Asian surge that has not happened yet.

**Blog drip: healthy, verified end to end.** The scheduled publish workflow has
fired daily and succeeded on all 27 runs. The September 14 post is live and the
September 16 post correctly 404s, which proves the deploy hook is wired, since
`main` has not moved. Every gap since the launch batch is exactly 2 days. The
one real problem was runway: the queue ended October 2. Five new posts take it
to October 12.

**Shipped:**
- `/international/`, the international applicant guide. Sources on every figure:
  the DHS final rule at 91 FR 44976 effective September 15 2026 (fixed period of
  admission up to 4 years, 60-day departure window cut to 30, graduate-level
  transfer and objective-change prohibitions), the pending NPRM at 91 FR 57807
  labeled as proposed, USCIS on OPT and STEM OPT, the DHS STEM list itself,
  USCIS on H-1B caps, the ICE $350 SEVIS fee, and the ETS surcharge schedule.
- `/apply/`, the application checklist. One deadline places 27 tasks on dates
  counted backwards, late items turn red, an international toggle adds 6 more
  steps, and the shortlist built on `/schools/` flows in over the same
  localStorage key. CSV export, print, no account.
- Rankings: an Intl column and filter group over class-profile data that was
  already sourced and simply never surfaced. 60 of 91 programs publish it;
  20 report 40 percent or more.
- `I18N.md` plus `src/i18n_audit.py`, which measures the translation surface
  instead of guessing at it, and a build guard that fails when page copy drifts
  into JavaScript where translation tools cannot reach it.
- `GROWTH.md` revenue section: the ad question answered with arithmetic.

**Access failures, reported rather than worked around:**
- `travel.state.gov` returns 403. The visa application fee, the interview
  process and the pre-arrival entry window are therefore absent from
  `/international/` rather than written from memory. Named explicitly on the
  page in a "what we could not verify" section.
- `mba.com` returns no page content to this environment, so no GMAT price is
  published on the new page.
- `help.raptive.com` returns 403, so the Raptive pageview minimum in GROWTH.md
  is flagged unverified rather than quoted.
- `federalregister.gov` redirects this environment to an unblock page. Worked
  around legitimately by using the official GPO text at `govinfo.gov` and the
  Federal Register API, both of which are authoritative.

**Tooling blocker from the last session is fixed.** Item 9 below was wrong about
the cause: the container does have `pdfminer.six`, and the broken `cryptography`
import was a missing `_cffi_backend`. `pip install cffi` repairs it, after which
PDF text extraction works. Used it this session to read the Federal Register
rule, the DHS STEM list and India's DPDP Act. The SAT percentile PDFs are
therefore no longer blocked.

### Next session queue (this session's additions)

1. Fill the 31 missing `intl_pct` values in `data/schools/` so the new
   international filter covers the whole table rather than two thirds of it.
   Protocol and merge tool are in `data/research/`.
2. Non-US programs in the rankings (INSEAD, LBS, IIM, ISB, HKUST, CEIBS and
   peers). Needs an owner decision first, because the SFN Score's salary band
   is calibrated on US dollar reporting and mixing currencies into one
   composite without a PPP adjustment would be dishonest. Recommendation: a
   separate international list rather than merging into the US composite.
3. SAT percentile content, now unblocked by the PDF fix above.
4. Owner decisions outstanding: flip `PAYMENTS_LIVE`, apply
   `PROPOSED_exam_states.sql`, and the undergrad rankings scope question.
