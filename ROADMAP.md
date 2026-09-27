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

### Later the same day: answer choices, and LSAT conclusions

- [x] **PR 97**: 165 hand-written distractors were garbled where a length-correction clause
      met the choice it extended (INC-0119), and 287 generated SAT and ACT word problems
      printed their unit twice (INC-0120). `bank_emit.extend` and `bank_repair.py` now refuse
      a needle that stops short of the end of its choice, and the build fails on any phrase
      said twice back to back.
- [x] **PR 98**: the same defect in the banks `bank_repair.py` lengthened in place, found by
      diffing the commit that applied it: 12 garbled distractors and 3 lost apostrophes
      (INC-0121).
- [x] **LSAT Drawing Well-Supported Conclusions** gets a generator, `src/gen/g_lsat_concl.py`:
      3,300 must be true items from statements using every, no, some and most, where the
      category had 31 hand-written items. Every key is proved by a checker that tries every
      group of up to three people of each of the eight kinds, and every wrong answer comes
      with a group in which it fails; the bound is checked against four on every build.
- [x] **GRE reading** gets generated items, `src/gen/g_gre_rc.py`: the same 27 passages shown
      as one paragraph of six sentences, with stated idea, main idea, caveat and a new
      function of a sentence question, 270 items where the category had 94 hand-written
      ones. The function questions ask about the four sentences that have to be read to be
      told apart, since every passage shares one shape.
- [x] **LSAT parallel reasoning**, `src/gen/g_lsat_parallel.py`: 150 items where Explanations
      and Parallel Reasoning had 29 hand-written ones. Eight argument forms, each proved valid
      or flawed by trying it against every small group; capped, because the category is also
      explanation questions, which stay hand written.
- [x] **Three new reading passages** (glacier retreat, orchard pollination, parish hymn
      singing), all with invented researchers and places: 30 more GMAT reading items and 29
      more GRE ones. The runner retires a schema after 400 duplicate draws in a row, which
      occasionally leaves the last unseen question of a small schema undrawn; that is why
      three passages gave the GRE 29 rather than 30.
- [x] **Two new long reading passages** (island depopulation and the ferry timetable,
      bridge pier failures and river scour), invented like the rest: 20 more GMAT reading
      items, 20 more LSAT ones and 21 more GRE ones, the GRE question the runner had left
      undrawn coming back with them. Adding them failed the build's length check on the
      LSAT caveat questions, 7 of 14 keys at the middle rank (INC-0122): a question asked
      once of each passage had its key's length rank drawn at random, so it passed or
      failed on the draw, and the GRE rotation added earlier the same day had been scoped
      to the GRE alone. Each passage's rank is now assigned from the ranks it can build,
      for the GMAT, LSAT and GRE variants alike, and a build check names any passage whose
      key is too long or too short to be placed.
- [x] **Why the Data Sufficiency schemas made different items on a second run** (INC-0123):
      all five, not the two the queue named, kept their count of answers produced on the
      schema for the life of the process, so a second run thinned against the first. The
      count is now tied to the rng of the run it measures, the banks are byte for byte what
      they were, and the build runs every planned schema twice from one seed and fails on
      any whose runs differ.
- [x] **Reviews waiting, on the daily pages** (GROWTH.md, what brings people back): each
      exam's daily page and the hub say how many flashcards the visitor has studied and is
      due to see again in that exam's trainer, read from the trainer's own progress in this
      browser and sent nowhere, with a link that opens the trainer on its flashcards
      (`/app/#cards`). The trainer and the daily pages take the trainer's storage key from
      one function in `src/daily_streak.js`, so they cannot come to read different places.
- [x] **A wrong fee in a live post** (INC-0124): the SAT vs ACT post's table gave the ACT
      science add-on as $4 while its own FAQ, ACT's fee page and `data/exams.json` say $5. The
      table is corrected, and the blog build now fails on any dollar amount in a post that
      appears nowhere in the sourced data, so a price has to be sourced before it is printed.
- [x] **Five more long reading passages** (borrowed vocabulary, pressed glass, a dye root
      trade, coastal storm records, hillside terraces), invented like the rest: 50 more GRE
      reading items, 50 more LSAT ones and 49 more GMAT ones, one GMAT stated idea question
      left undrawn by the runner's 400 draw cutoff.
- [x] **Two ACT posts for the blog drip**, after it ran out on October 12: how the Composite
      is calculated (October 14) and the 2026 format and fees (October 16), every figure read
      from act.org the same day or already sourced in `data/exams.json`. The EDITORIAL fact
      sheet gains an ACT block, and `data/exams.json` gains the rounding rule and ACT's
      superscore details with their page.
- [x] **Scorecard figures pointed at their own school** (INC-0125): every one of the 337
      College Scorecard earnings and debt figures in the MBA library cited the program's
      website as its URL, a page that does not hold the number. They now cite the
      Scorecard's data page, the enrichment script writes that URL, and the school
      validator checks the federal block and refuses a Scorecard figure whose URL is not
      on collegescorecard.ed.gov.
- [x] **LSAT principle questions, generated** (`src/gen/g_lsat_prin.py`): Principles,
      Rules and Analogy had 29 hand written items. The schema states a principle about a
      group (every member who P, or P and Q, should A; no member who P should A) and asks
      which of five judgments it establishes. A checker treats what should happen as
      required, forbidden or neither and tries every case the principle leaves open, so
      exactly one judgment is established, and it tells should not from need not, which
      the forbidding form would otherwise offer as a second key. The key had no negation
      in it and was the shortest or second shortest choice three times in four, so its
      length position is drawn first and the wrong answers and unrelated facts chosen to
      land it. Capped at 150, because the category is also identifying principles and
      analogy, which stay hand written.
- [x] **Two "good score" posts for the blog drip**, the kind of page answer engines cite
      most: the ACT (October 18) from ACT's national ranks for tests taken September 2026
      through August 2027, and the GRE (October 20) from ETS's interpretive data for
      everyone who tested July 2022 to June 2025. Both tables were read from the test
      makers' PDFs today, every figure in the posts was checked against them, and the ranks
      are mirrored in `data/exams.json` and the EDITORIAL fact sheet. The two define a
      percentile differently (ACT counts scores at or below, ETS scores below), and the GRE
      post says so.
- [x] **A "good SAT score" post** (October 22) from College Board's dated figures rather
      than its undated percentile tables: the 2025 SAT Suite Annual Report for the class of
      2025, 2,004,965 students at their most recent score, mean 1029. The distribution page
      was cut from the PDF and read as an image to confirm the counts, which sum to the
      class total in every column; the post's shares are arithmetic on those counts. Reading
      PDFs here needs `pip install pdfminer.six cffi pypdf` in the container.
- [x] **A "good LSAT score" post** (October 24) from LSAC's percentile table for the
      2023-2024 through 2025-2026 testing years, which LSAC publishes as HTML, so all 61
      rows were parsed and every figure in the post checked against them. Two details the
      search summary offered (the July to June testing year and a summer update) are not on
      LSAC's page and were left out.
- [x] **Five more long reading passages** (hilltop beacons, a silk trade, early printing,
      water mills, river mussels), invented like the rest: 50 more LSAT reading items, 51
      more GMAT ones (the question the runner left undrawn last time came back) and 49 more
      GRE ones (one left undrawn this time by the same 400 draw cutoff). Proofreading moved
      three trailing "whether or not" clauses to the front of their findings, where the
      "is unreliable" wrong answer had run straight into them.
- [x] **Every reading question, every build** (INC-0126): the runner retired a schema after
      400 repeats in a row, and that left one reading question undrawn on three of the four
      passage builds above. Each reading schema now lists the questions it can ask, from the
      same list its draws come from, and so do the two LSAT argument structure schemas, which
      are built the same way. The runner retires such a schema once it has made them all,
      and the build fails if a category under its target is missing any of them. The GRE
      gets back the guilds question it had lost (20388 items). No other questions changed;
      some reading and structure items were drawn with different wrong answers.
- [x] **Generated items keep their ids from build to build** (INC-0127): an id was the
      item's position in the build, so any bank change renumbered what came after it. The
      fix above alone would have pointed 6826 live ids at different questions. The trainer
      keys spaced reviews and item telemetry on those ids, so a review due for a missed
      question could serve another one. An id is now the exam's prefix and twelve hex digits
      of the item's content key, and the build fails if one does not match its item or two
      items share one. Old numbered ids stored in a browser named different questions in
      different builds and cannot be mapped back, so the trainer drops review and seen
      entries of that form once, on load.
- [x] **Each exam guide's trainer button opens that exam's trainer** (INC-0128): the Train
      for It Here button at the foot of the SAT, GRE, LSAT and ACT guides opened the GMAT
      trainer, because it was the literal `/app/` while the header button read the map of
      trainers. The study guide hub, which covers all five exams, had one button to the GMAT
      trainer too; it now has one per exam. The build fails if an exam page links to any
      trainer but its own, or if the hub misses one.
- [x] **The playbook's rules digest holds its own word budget** (INC-0129): adding the
      128th incident took the bootstrap digest to 4012 words against its 4000 word limit,
      the same failure INC-0083 fixed at 82 by shortening each rule, which left the digest
      still growing by a rule per incident. The generator now keeps every rule learned more
      than once, then the rest by severity while they fit, and says how many it left out;
      the checklist in the book still carries every lesson.
- [x] **ACT score calculator** at `/exams/act/score-calculator/` (GROWTH.md, next #2): the
      Composite and superscore worked by ACT's published rule, with the national rank for
      the Composite and ACT's full 2026-2027 national ranks table. The table is parsed from
      ACT's own PDF by a script into `data/act_national_ranks.json` (the live PDF matched the
      copy read for the good ACT score post byte for byte), checked at build time and cell
      by cell in the browser by `src/smoke_calculator.js`. The ACT guide and both ACT posts
      link to it, and the sitemap now lists pages under an exam's guide.
- [x] **Every exam fact checked against the page it cites** (INC-0130, INC-0131, INC-0132):
      the GRE guide credited ETS with a combined 260 to 340 score its cited page never
      mentions, so `src/check_sources.py` now reads every page and PDF `data/exams.json`
      cites and reports each number the source does not print. Its first run found the GRE
      fee still at $220 when ETS's has been $249 since August 1, 2026, fee notes carrying
      clauses their pages do not say, two ACT claims cited to the wrong page and two that
      are on no ACT page, and a GRE law school count that said ABA-approved where ETS does
      not; each was corrected against its page, posts included. It runs weekly in the
      playbook workflow and opens an issue when a figure stops matching. Tracing the GRE
      text also found the `/exams/` hub's structured data printing a Python dict as every
      exam's description; the build now fails on any page that prints one.
- [x] **GRE score calculator** at `/exams/gre/score-calculator/`: where a Verbal,
      Quantitative or Analytical Writing score stands in ETS's percentile ranks (the percent
      scoring lower, July 2022 to June 2025), with the full tables, from ETS's interpretive
      data PDF parsed into `data/gre_percentiles.json`. The text layer drops ETS's blank
      cells, so the columns were aligned against the rendered table and the build rejects a
      blank above a reported score. Verbal plus Quant is shown only as arithmetic, with no
      percentile, because ETS reports and ranks the three scores separately.
- [x] **SAT score calculator** at `/exams/sat/score-calculator/`: the table the queue was
      waiting on is on College Board's research site
      (research.collegeboard.org/reports/sat-suite/understanding-scores/sat, last modified
      September 15, 2026), with a nationally representative and a user group percentile for
      every total from 400 to 1600 and every section score from 200 to 800. It is parsed by a
      script (`src/sat_percentiles.py --write`) into `data/sat_percentiles.json` with the
      page's definitions quoted verbatim, and the total rule is the fall 2026 Understanding
      Scores guide's "Sum of the 2 section scores". The weekly source job runs `--check`,
      which re-reads the page and opens an issue when any cell or definition changes. The page does not say which three cohorts the user group covers, so the site
      does not either, and it does not claim either group is the All Tester Percentile on a
      score report. The SAT guide, the SAT vs ACT post and the good SAT score post link to it.
- [x] **PSAT/NMSQT calculator** at `/exams/sat/psat-calculator/`: the total and the NMSC
      Selection Index, (2 x Reading and Writing + Math) / 10 on 48 to 228, from the fall 2026
      PSAT/NMSQT Understanding Scores guide and College Board's scores page, with College
      Board's percentiles for 10th and 11th graders from its research site and the guide's
      grade-level benchmarks. The research page gives each section table's grade only in
      the heading printed before it, so the parser reads that heading rather than trusting
      the order, and it records the reading column's heading as printed ("Evidence-Based
      Reading and Writing", "EBRW"), which the page notes. No National Merit cutoff is
      estimated. `sat_percentiles.py --check` covers both pages weekly.
- [x] **LSAT percentile calculator** at `/exams/lsat/percentile-calculator/`: LSAC's Data
      Library table (every score 120 to 180, percent of test scores below, 2023-2024 to
      2025-2026 testing years) parsed by `src/lsat_percentiles.py`, looked up both ways. The
      build checks that the three precisions LSAC prints agree; its whole-number column
      stops at 99, which the page notes. Linking it from the queued LSAT format post found
      that post calling the live LSAT trainer "in development" (INC-0137) and repeating a
      delivery claim LSAC had overtaken, which was also live in the LSAT guide (INC-0136):
      both fixed, and the blog build and the weekly source check now catch each kind.
- [x] **Score calculators on the `/exams/` hub** and under Resources in the site menu: one
      card per calculator, generated from the `CALCULATORS` map the exam guides use, so a
      new calculator appears in both places or the build fails for want of its line. Adding
      it found the hub's meta description still saying only the GMAT and SAT trainers were
      live (INC-0138): it is now built from `LIVE`, and every built page is checked for a
      sentence that calls a live trainer unfinished.
- [x] **"What Is a Good PSAT Score in 2026?"** queued for October 26, the next free drip slot:
      College Board's percentiles for 10th and 11th graders, the grade-level benchmarks and
      the Selection Index, every figure generated from `data/psat_percentiles.json` and
      checked against it by script, with a PSAT/NMSQT block added to the EDITORIAL fact
      sheet. It estimates no National Merit cutoff.
- [x] **Two MBA posts queued from the verified school library**: "How Much Does an MBA
      Cost? 2026 Tuition by School" (October 28) sets 2026-27 tuition at twelve two-year
      programs beside what it leaves out, the two prices public programs charge, and the
      schools that price the whole program; "MBA Employment Rates: How to Read the 3 Month
      Number" (October 30) shows the same classes counted at three and six months, and as
      offers received and accepted. Every figure comes from a school record the source
      check read and matched, both have EDITORIAL fact sheet blocks, and a script checked
      each number in them against those records. Stanford's employment page is built by
      JavaScript, so it is left out until the weekly rendered run reads it.
- [x] **Blog pages get the design tokens** (INC-0139): `build_blog.py` pasted the shared
      header and footer CSS without `TOKENS_CSS`, so all 32 blog pages used 22 tokens they
      never defined and the logo sat against the screen edge on phones. The blog now injects
      the tokens as `apply_chrome` does, and the build fails on any page that uses a token
      it never defines.
- [x] **Whole program cost for 19 schools that never price a year**: `program_cost_usd`
      holds the figure a school publishes for the whole program (a total, a program fee or
      an estimate of the whole), shown in its own row, sentence and Quick Answer, in the
      rankings drawer, the CSV export and the trainer's fit card (compared against a budget
      as it stands, with no two-year arithmetic). It never enters the SFN Score, the tuition
      column or the tuition filter, and a per-credit rate is never multiplied out. Every
      figure was read from the school's own page and passes the source check (671 facts on
      243 pages). The school pages gain Cost in their titles. Oklahoma Price's full-time MBA
      moves to Oklahoma City, where its page says it meets. Not filled: Fordham (its tuition
      page loops on redirects from here), Texas A&M (its page does not say whether its
      figures are a year or the whole program), Iowa, Missouri and UConn (their full-time
      programs closed), and Northeastern, Purdue, Syracuse, San Diego and Temple (per-credit
      rates only, or a JavaScript calculator).
- [x] **Each employment rate says when it was measured** (INC-0142): every figure was
      labelled "Employed at 3 months" and scored as one, though 15 of 70 were measured at
      six months, four months, a year or a reporting date, or at a timing not yet verified.
      The label now comes from each figure's own note; a rate measured at another point is
      shown with its timing and neither scored nor sorted with the three month rates, as the
      methodology says, and an unverified timing is labelled so and still counts. UNC moves
      to the three month rate its report prints (88 percent). The SFN top three are
      unchanged; Michigan State (93 percent at six months) goes from 26th to 43rd and Tulane
      (100 percent at four months) from 36th to 51st. Still to verify: the timing of
      Wharton's, William & Mary's and Portland State's rates (Wharton's report is unreadable
      from here).
- [x] **Six figure descriptions moved where the pages print them** (INC-0143): Booth's,
      Tepper's, Michigan Ross's and Penn State's tuition, Emory's acceptance rate and
      Vanderbilt's salary carried their description under `note`, our commentary, so their
      pages showed them bare and the source check never read them. They are now `stat`, and
      the validator refuses a note without one. Vanderbilt's note, cut off at "plus", is
      whole again, and its salary keeps Bloomberg's median as a secondary figure because the
      school's own page prints only "$148K+".
- [x] **BYU Marriott's two-year total is no longer tuition a year** (INC-0144): its page
      prints $63,968 as tuition for the entire two-year program (members 31,984), which the
      library held as tuition per year, so the page, the tuition column and the fit card's
      two-year arithmetic all doubled it. It is now a whole program cost, and the validator
      refuses a yearly tuition whose note calls it a program total.
- [x] **The school library checked against its sources** (INC-0133): `check_sources.py
      --schools` reads every page the library cites (652 figures, 225 pages; the 337 College
      Scorecard figures come from a dataset and are set aside). Reading its flags on static
      sources found Columbia's GRE Verbal and Quant each recorded as 163, half the combined
      326 its article prints, and Miami Herbert's GMAT median and share of women, which its
      news story never mentions; all three are now blank. Honest conversions (months to
      years, a count to a percentage, a rounded GPA, $100k over two years) now declare their
      working, and the checker reads $175K, 30-70 k and 2026-27 the way pages print them.
      The school check runs weekly with the exam check, rendering pages built by JavaScript.
- **Decided against** mapping the two paragraph passages onto GRE reading as they are. ETS
  says most GRE passages are one paragraph long (ETS, GRE General Test Verbal Reasoning,
  https://www.ets.org/gre/test-takers/general-test/prepare/content/verbal-reasoning.html, read
  September 26, 2026); ours are two paragraphs of 202 to 442 words, and thousands of them would turn
  the GRE reading mix upside down. That is why the GRE items above show them as one paragraph.

- [x] **LSAT Argument Parts and Structure** gets a generator, `src/gen/g_lsat_struct.py`: 30
      arguments written with their parts labelled (a rejected view, the main conclusion, an
      intermediate conclusion and two premises), rendered so the connecting words fix each
      part's role, asked about as 150 role questions and 30 main conclusion questions where
      the category had 30 hand-written items.

### Next session queue

- [ ] More reading passages: every reading category is still far under target, and each
      passage adds ten GMAT items and ten GRE items, plus ten LSAT items at LSAT length
- [ ] Read the hand-written reading items against the same two checks (the rule is printed;
      no choice is answerable by matching words); they were not part of this pass
- [ ] Refresh the remaining class profiles as schools post their fall 2026 classes; MIT Sloan
      first, once its page can be read. Checked September 26: the class profile pages of HBS,
      Stanford, Wharton, Booth, Kellogg, Yale, Tuck, Haas and Darden all still show the Class
      of 2027, so there is no newer class to publish yet; recheck in October. HBS, Booth,
      Yale, Tuck and Haas were read against the library and match it (Booth's page carries a
      stale Class of 2026 block beside the 2027 one, which a text summary conflates; the raw
      page confirms the library's figures)
- [ ] `src/smoke_load.js` stays out of CI because timing on shared runners is noisy, so run
      it by hand after any change to how the banks are split or loaded (INC-0113)
- [ ] School figures the `--schools` run could not settle from this sandbox. The last run of
      September 27 ends at 40 figures with a number their page does not print, 20 sources
      unreadable and 9 showing none of their figures. Rice's, UVA Darden's and Foster's
      employment rates now declare the printed shares they sum, BYU's rate is printed in
      words, and Rutgers carries its Class of 2025 outcomes (82.6 percent employed three
      months after graduation and a $105,000 median base salary) in place of a 2020-2024
      average its page no longer prints. Most of what remains is on pages that draw their
      figures with JavaScript (Haas, Kellogg, Rice's class profile, Pitt, UCSD), plus years a
      note gives for context that the page itself does not print. Tuition is down from 23 of those to 3:
      Booth, Tepper, Willamette and Georgia Terry now cite their 2026-27 pages, every tuition
      sum declares its working so the check verifies the inputs (INC-0140), and two notes the
      research merge had cut off at 300 characters are whole again (INC-0141). USC Marshall's
      and William & Mary's tuition pages draw their figures with JavaScript, and Cincinnati's
      out-of-state surcharge sits on a second UC page, named in its notes. From 2026-27 UC
      bills the Lindner MBA per credit hour and the program runs 35 to 48 credits, so
      Cincinnati keeps its labelled 2025-26 figure until the school page can show a range.
      Georgetown and Ohio State Fisher now carry the classes that entered in 2026,
      read from their own pages, and MIT Sloan's class size is its Class of 2028 figure; the
      rest of MIT's Class of 2028 profile is drawn by JavaScript, so it waits for the weekly
      rendered run (the posts quoting its Class of 2027 figures name that class, so they stay
      correct). Pages whose figures render by JavaScript (Stanford, Kellogg, Haas, Kelley,
      Rady and others) are for the weekly job, which reads them with Chromium. UCSD's Rady
      tuition now reads UCSD's 2026-27 fee page, the 2025-26 one being gone. Unreadable from here: 403s at Columbia, Baylor, Michigan
      Ross and Bloomberg, certificate failures at Penn State Smeal and UC Irvine Merage (not
      to be bypassed), US News, Fordham redirects and ASU (522)
- [ ] Emory Goizueta's acceptance rate (32 percent, from Poets&Quants) disagrees with its own
      source label: 450 admitted of 1,581 applications is 28.5 percent, and the record's
      notes call the 32 percent "Poets and Quants math" with no official counterpart.
      Poets&Quants answers 403 here, so the figure is unchanged and flagged to the owner;
      read the article, then correct the value or the label.
- [ ] Six GMAT facts cite pages this sandbox cannot read: four on www.mba.com serve a bot
      challenge and two on support.mba.com answer 403. check_sources reports them as
      unreadable, not wrong. The weekly job may read them from GitHub's runners; if it
      cannot either, find the same figures on gmac.com and move the citations (INC-0100
      did this for the section table)

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
