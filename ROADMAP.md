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
- [x] **"GRE Scores for Top MBA Programs: 2026 Guide"** queued for November 1: thirteen
      schools' verified class GRE figures (158 to 166 Quant, 159 to 164 Verbal, each labelled
      median or average and by class) beside ETS's percentiles, which put a 164 at the 63rd
      percentile in Quant and the 93rd in Verbal, and the share of HBS's and Booth's classes
      that submitted a GRE. Checking Wharton's row found its page crediting its Class of
      2026 GRE scores to the Class of 2027 (INC-0145): the GRE sentence began with Its and
      took the class named before it. GRE now goes through the class sentences, and a lead
      sentence that opens with Its fails the build.
- [x] **Five more long reading passages** (a downland moth, a port's tide predictions,
      upland cattle fairs, how village names were said, a change in pottery), invented like
      the rest of the corpus, each a revision narrative with its two rules printed. The
      banks grow by 50 GMAT, 50 GRE and 50 LSAT items (GMAT 34062, GRE 20438, LSAT 14342 of
      which 13970 are generated), and llms.txt and the EDITORIAL product facts carry the new
      counts. A sample of every question type from the new passages was read for seams;
      the one "whether or not" finding opens its clause, so the "is unreliable" distractor
      does not run into it.
- [x] **The source check reads class profiles drawn in embedded charts** (INC-0146). Its
      browser read waited for a quiet network that pages with trackers never reach, never
      scrolled, and read only the top frame, so Stanford's class profile, an Infogram chart
      that draws its numbers only when scrolled into view, came back with no figures.
      `src/render_page.js` now scrolls, reads every visible frame, skips hidden frames and
      PDFs, and has one deadline; `src/smoke_render.js` holds a local page with each trait.
      The session sandbox's browser trust store also lacked the egress proxy's CA, so no
      page could render here; adding it with certutil (verification stays on) lets the
      check render in a session as well as in the weekly job, and each new sandbox needs
      it added again until the environment's setup script does it. First
      results: Wharton's own page gives its Class of 2027 profile (GPA 3.7, GMAT Focus 676,
      Classic 735, GRE 163 and 162, 888 students, 44 percent women, 26 percent international),
      which replaces the Class of 2026 section and Poets&Quants' Focus figure, and MIT Sloan's
      gives its Class of 2028 (median GPA 3.74, median GMAT Focus 675 with a middle 80
      percent of 645 to 715, 45 percent international, 43 percent female), updated September
      2026. The queued GRE post and the fact sheet carry Wharton's Class of 2027 scores and
      add Stanford's (164 Quant and 164 Verbal, Class of 2027), now read on its own page.
- [x] **A bare year no longer names a class** (INC-0147). Six records stored a class label
      that was only a year, which the site printed as a Class of that year: Notre Dame's
      page said "The Class of 2027 has 85 students" from a program page that prints an
      average cohort size of 85 and names no class, and Penn State Smeal's credited the
      Class of 2025 with a GMAT from a 2020 report on its legacy two-year MBA. Maryland and
      Texas A&M now read Class of 2026, the class their Poets and Quants figures describe;
      Notre Dame and Florida say no class year is stated; Georgia Terry, with no class
      figures, has no label; Penn State's legacy GMAT, GPA and salary are removed. A figure
      whose stat says its page labels no class year now takes none, the validator refuses
      a bare year, and the class self-check covers both.
- [x] **"Average GPA for MBA Programs: 2026 Class Data"** queued for November 3: every
      program in the library whose GPA figure names a class that entered in 2025 or 2026
      and matched its page in September 2026, 37 in all, from 3.28 at Boston College
      Carroll to 3.76 at Harvard Business School and Stanford GSB, each labelled average,
      median or mean and by class, with the ranges that put admitted students well below
      the averages and the schools whose figure counts only 4.0-system or domestic GPAs.
      A program whose page names no class year is left out rather than given one, which
      is how INC-0147 surfaced.
- [x] **"How Much Work Experience Do You Need for an MBA? 2026 Class Data"** queued for
      November 5, on the same rule: 38 programs, from 17.1 months at College of
      Charleston's one-year MBA to 6 years at seven programs, with the middle program at
      5.1 years. It quotes Wharton's page that there is no minimum or maximum, the ranges
      that reach 0 years (NYU Stern, Colorado Leeds, Boston College Carroll), and the four
      programs built for fewer years.
- [x] **supabase-js is served from this site** (INC-0148). The trainer apps, the community
      page and the do-not-sell page loaded it from cdn.jsdelivr.net as a blocking script,
      so none of the app's own code ran until jsdelivr answered, and a slow answer timed
      out CI's games smoke. It now comes from /vendor/ (2.117.2, the build jsdelivr served,
      MIT license alongside), the CSP drops jsdelivr from script-src, and both builds fail
      on any page that loads a script from another host. Fonts still come from Google
      (DEVSECOPS.md O6).
- [x] **A half-typed sign-in survives a redraw** (INC-0149). Each deferred bank chunk redraws
      the Account page to update the bank size it prints, and the redraw rebuilt the sign-in
      form from saved settings, so an email typed before pressing Send came back empty.
      src/smoke_signup.js had been failing on that for as long as it sat outside CI. The form
      now keeps what its fields hold, the smoke checks a forced redraw directly, and it runs
      in npm run test:browser.
- [x] **Columbia's work experience was another program's** (INC-0150). The record's five years
      is the MBAxMS cohort's in the cited Poets&Quants article, which gives none for the MBA
      class; the source check passed it because the article does say five years. It is empty
      now, and the queued work experience post drops Columbia (37 programs, 28 between 4.9 and
      6 years, the middle one still 5.1). The school check now wants each figure's number beside
      a word saying what it counts, and lists a figure found only near another program's name
      for a person to read: 13 today, 12 of them the right program's figures. The 13th, Rice's
      international share, has no support on Rice's page, which now prints three-year
      averages, and Rice is already queued for a refresh.
- [x] **Two more class data posts queued** on the same rule, now with each figure found beside
      its label: "Women in MBA Programs" (November 7), 35 programs from 24 to 56 percent with
      the middle class at 43, and why MIT reports female; "International Students in MBA
      Programs" (November 9), 35 programs from 10 to 63 percent with the middle class at 37,
      what Tuck, Duke and Miami each count as international, and Columbia's fall from 46 to 41
      percent. Rice stays out of both until its page is read again.
- [x] **Rice moves to the three-year averages its page shows, and its GMAT was never
      Poets&Quants'** (INC-0151). Rice's class profiles page now gives only an average of the
      Classes of 2026, 2027 and 2028, behind its Full-Time MBA button, so the record carries
      those figures labelled as that average (134 students, a 3.46 GPA, 5.4 years of work
      experience, 36 percent women, 33 percent international, GRE 159 Quantitative and 157
      Verbal), and its page says "Averaged over the Classes of 2026, 2027 and 2028, a class has
      134 students" instead of naming one class. Its GMAT of 693, cited to Poets&Quants' Class
      of 2027 article, is not in that article, which gives a median of 700; the figure's note
      said it was read from a search snippet. Neither that median nor the page's 694 names an
      edition, so Rice shows no GMAT. The validator now refuses a figure whose stat, note or
      source says snippet, and UNC's and USC's GMAT notes, the other two, quote their articles.
- [x] **The source check no longer reads HTML comments** (INC-0152). It kept the text inside
      comments as page text, so a figure a school had commented out still counted as
      printed: Arizona State's 43 percent women sits only in a hidden row, and its page shows
      no gender figure at all. Comments are dropped before the page is read, the self-check
      holds a commented-out row, ASU's women share is empty, and the queued November 7 post
      drops ASU (35 programs, the middle class still 43 percent women). Rerun without
      comments, the exam check's 79 facts come out the same, and ASU's is the only school
      figure that changes.
- [x] **School pages say why no GMAT is shown.** 44 school pages have no GMAT figure: some
      schools print none, and some print one without naming its edition, which is never
      guessed (INC-0151). Those pages used to drop the GMAT rows without a word, though the
      average GMAT is one of the questions they are searched by. They now carry one GMAT row
      marked not verified, as the acceptance rate row does (INC-0118), and a Quick Answer
      that says so and gives the program's GRE scores where it has both.
- [x] **"MBA Salary by School" queued for November 11**: median salaries for graduates of
      2025 at 26 programs, from $105,000 at Rutgers to $185,000 at Stanford GSB and Wharton,
      13 of them at $175,000 or more, each read on its page (Kellogg's in a browser, since
      its page draws the figure with JavaScript). Wharton's and Booth's own reports cannot be
      read from here, so theirs come from Poets&Quants' M7 report, as do Harvard's and
      Columbia's. Left out and said so: averages, pooled classes, SMU Cox (its page calls the
      same $126,000 an average and a median) and BU Questrom (its report's text does not show
      which figure is the median). Michigan Ross's salary gains the stat its article prints.
- [x] **Five school pages name their school** (INC-0153). Charleston, Lehigh, Portland
      State, UC Davis and UC Riverside were named "School of Business", "College of
      Business" or "Graduate School of Management", which the page printed alone in its
      title, heading and answers ("School of Business MBA: Cost and Class Profile"). Each now
      carries a standalone name its own site uses (Charleston School of Business, Lehigh
      College of Business, Portland State University School of Business, UC Davis Graduate
      School of Management, UC Riverside School of Business), and the validator refuses a name
      made only of generic words.
- [x] **Test dates for the SAT, ACT and LSAT** at `/exams/<exam>/test-dates/`, parsed by
      `src/test_dates.py` from College Board's, ACT's and LSAC's own tables: 8 SAT Weekend
      dates, 7 ACT national dates and 13 LSAT administrations, with the in-school SAT and
      PSAT windows and next year's anticipated and projected dates. Each page leads with
      where registration stands on the reader's own day, the next date still open (regular
      or late) and any nearer test whose deadlines have passed, because the next test date
      alone can be one a student can no longer register for. Every date downloads as a
      calendar file holding its deadlines and test day, with reminders. The build refuses a
      row whose dates run out of order, the weekly source job re-reads all three tables, and
      `src/smoke_dates.js` checks the note on four different days and every calendar file
      against the row it came from. Linked from each exam guide, the /exams/ hub, the
      Resources menu and llms.txt.
- [x] **Every school figure the source check flagged is fixed or judged** (INC-0154). The
      weekly check listed 30 figures their pages do not print, and 13 were wrong or out of
      date. Duke's GMAT Focus 665 and Classic 720 medians were never printed by the GMAC
      article they cite, and Duke's own Class of 2028 page gives only a middle 80 percent range
      of 605 to 715, so Duke's GMAT is blank. Michigan Ross's 5.8 years of work experience is
      in no source (blank), and Ross gains the article's GMAT Focus average of 681, both GMAT
      figures now carrying its edition labels. WashU Olin's $130,000 salary sat beside the
      Class of 2024 report, which gives $126,000; Olin now carries that report's median and its
      78 percent accepting a job within three months (81 percent with an offer). Darden's
      "middle 80 percent" ranges are the page's Low and High. Boston College's class size and
      acceptance rate and Wisconsin's women and international shares are blank, their pages
      no longer printing them; USC's tuition is its 2026-27 $86,295; William & Mary's says its
      page names no year. The check now reads an image's alt text, where Berkeley Haas and
      Pitt Katz print their figures, and a second page named in `also_urls` (Cincinnati's
      surcharge). Kellogg's middle 80 percent ranges, drawn only as box plots, are recorded in
      `data/source_triage.json`: the check lists triaged figures apart and fails only on a
      finding nobody has judged, and validate_schools refuses an entry once its figure changes.
- [x] **The GMAT guide's free score report rule cites the page that states it** (INC-0155):
      "up to 5 free score reports ... within 48 hours" linked to mba.com's Official Score
      Reports page, which never mentions them; it now cites the Sending Your Score page. The
      source check no longer reads a bot challenge as the page it stands in for (INC-0156):
      mba.com's Imperva challenge, 726 characters, had passed the 400 character floor, so a
      right fact was reported wrong. A challenge is now reported as an unreadable source and
      never cached.
- [x] **Every GMAT figure says which edition its source gives it** (INC-0157). Eleven
      figures on ten school pages had been filed under an edition their sources never name,
      by guesses printed beside them, some false ("above Focus scale cap" for 698 and 702,
      though the Focus scale runs to 805). They are blank, each with a note quoting what its
      source prints: Georgia Tech, Washington Foster, UC San Diego Rady, Arizona State (both),
      Texas A&M, William & Mary, Notre Dame, USC Marshall, UNC Kenan-Flagler's Classic figure
      and Cornell, whose own FAQ calls the current exam plain "GMAT". Thirteen whose pages do
      name the edition now say so in the page's words, WashU's stays on its page's 200 to 800
      scale, and Babson, Kentucky, Northeastern and TCU keep theirs with an `edition_proof`:
      each class enrolled before Focus testing began on November 7, 2023. validate_schools
      refuses a GMAT figure that shows neither its source's label nor a proof.
- [x] **"Average GMAT Score by MBA Program" queued for November 13**, Maya Chen: every
      verified GMAT figure for a class that entered in 2025 or 2026, each edition in its own
      table (GMAT Focus at 25 programs, 541 to 690; Classic at 21, 650 to 740), with why
      classes report two editions (Focus testing from November 7, 2023; scores valid five
      years), Chicago Booth's split of who submitted which, GMAC's percentile concordance,
      averages against medians, and the ranges that reach below every headline figure.
      Harvard's GMAT stats gain the middle 80 percent ranges its page prints. The fact block
      is in EDITORIAL.md.
- [x] **Five more long reading passages** (an observatory's star catalogue, cracked
      cathedral glass, fever in a port town, a region's fiddle tunes, the fineness of a
      flock's wool), invented like the rest of the corpus, each a revision narrative with its
      two rules printed, 300 to 330 words. The banks grow by 50 GMAT, 50 GRE and 50 LSAT
      items (GMAT 34112, GRE 20488, LSAT 14392 of which 14020 are generated), and llms.txt and
      the EDITORIAL product facts carry the new counts. Every question type from the new
      passages was read at GMAT, GRE and LSAT length; the source phrase the distractors reuse
      lost its trailing "house by house", and names that other passages already use (Merrow,
      Ferrand, Maddox) were changed so that no two passages share a researcher or a place.
- [x] **Kelley moves to its Class of 2028, and a page showing none of its figures is a
      finding** (INC-0158). The source check had written off six pages as probably built by
      JavaScript, and only WashU Olin's, drawn as images, was. Kelley's page had moved on to
      the Class of 2028 (57 students, GMAT 618, GPA 3.38, against the library's 106, 607 and
      3.48); Poets&Quants' Maryland profile, updated September 25, now gives 36 percent women
      and 47 percent international, not 35 and 68, and its enrollment of 115 does not say
      whether it counts one class, so Maryland's class size is blank; Auburn's counters now
      stop at a 3.47 GPA and 1.81 years and give no international share; UMass's PDF glued
      each figure to its label and dates from August 2025, not 2023; Booth's report is an
      Excel workbook. The check now reads counters, glued figures and workbooks, lists a
      blank page with what it prints beside each label, and fails the run on it until every
      figure is fixed or triaged. WashU's eight image figures, five of them new (44 percent
      women, 47 percent international, 4.3 years, GRE 166 and 164), were read from its
      images and triaged.
- [x] **Baylor's class size counts its full-time students, and refused pages are read in
      the browser** (INC-0159). Baylor's 80 was the whole MBA program's entering class, 15
      of them part-time, under a note naming only the two full-time tracks; its acceptance
      rate of 24.4 percent was the same total, with all 15 part-time applicants accepted. The
      class size is now 65 (53 two-year and 12 one-year) and the acceptance rate 22.1 percent
      (106 of 480), each with its working, and the whole-program GPA, women and
      international figures say so. The source check reads a page that refuses its plain read
      in the browser, which opens Baylor's pages; Columbia, Michigan Ross and Bloomberg answer
      the browser with a bot challenge, now recognised and reported as one.
- [x] **"How Much Does the GMAT Cost in 2026?" queued for November 15**, Sarah Whitfield:
      the US fee table from mba.com's exam payment page ($275 at a test center, $300 online,
      $35 per extra score report), the rescheduling and cancellation schedules with what each
      costs as a share of the fee, the 24-hour rule, free score reports, fee waivers and
      vouchers. The GMAT guide's Cost tile had shown $275 and $300 from the note of a cost with
      no value, cited to a register page that prints no price and read by no check (INC-0160);
      the cost now has its value and the fee table is a set of checked key facts, read from the
      address mba.com loads its US table from. The source check's blank-page rule now reads a
      figure against every page it names (INC-0161), and a browser read that gets a challenge is
      tried once more.
- [x] **"How Much Does the GRE Cost in 2026?" queued for November 17**, Elena Rodriguez:
      ETS's fees ($249 outside China and India, $231.30 in China, $55 to reschedule or change
      test center, $40 per extra score report, $60 Analytical Writing review, $50 score
      reinstatement), the one deadline for rescheduling and the half refund, four free score
      recipients, the non-refundable 4% online service fee and the taxes added in the United
      States, and the fee reduction. The GRE guide gains five key facts from ETS's fees page and
      the 2026-27 Bulletin, checked weekly. ETS values its free prep bundle at $110 on one page
      and $100 on two others, so the post quotes the items, not a total.
- [x] **"How Much Does the LSAT Cost in 2026?" queued for November 19**, Aisha Thompson:
      LSAC's fees ($253 for the LSAT with Argumentative Writing, $219 for CAS, $45 per law
      school report, Score Preview $46 or $87, a $50 candidate score report, a $150 Score
      Audit), what applying costs in LSAC fees ($517 for one school, $697 for five, $922 for
      ten), the test date change steps (free, $153, $253), the refund rules (full through the
      refund deadline; no CAS refunds since May 20, 2024) and the two fee waiver tiers. The
      LSAT guide gains five key facts from LSAC's fees, refund and fee waiver pages, checked
      weekly. With the GMAT and GRE posts this makes a three-post run on what each test costs.
- [x] **Fordham's pages are read in the browser.** They send a script round a login
      gateway's redirect loop, so the source check reported them unreadable; it now gives a
      redirect loop the browser read it gives a refusal, and all four Fordham figures verify
      (59 percent international, 39 percent women, 5.3 years, and 85 percent of the Class of
      2025 seeking work accepting offers within 3 months). Fordham's record now says which of the page's two MBA blocks
      its figures come from.
- [x] **"How Much Does the SAT Cost in 2026?" queued for November 21**, David Okafor:
      College Board's fees ($68 in the US, $111 abroad with the $43 international fee, a $24
      test center fee at listed centers, $38 late registration, $34 to change test center or
      cancel by the change deadline and $44 later, 4 free score reports within 9 days and $15
      each after), what cancelling gives back ($34, or $24 late), and the fee waiver's
      benefits. The SAT guide gains five key facts from College Board's fees, international
      fees, refunds and fee waiver pages, checked weekly. The blog build had refused the post
      (INC-0162): its check that a post never calls a live trainer unfinished read the fee
      table as one sentence, and College Board's seat Waitlist sat in it beside the SAT's fee.
      It now splits a post at block elements, as the built-page check does.
- [x] **Each exam guide links to its exam's posts.** The five exam guides linked to no
      post at all, so the cost and good-score posts had no link from the pages that rank for
      their exams. Each guide now ends with "From the Study Room": up to six published posts
      whose slug names the exam, newest first. A post joins its guide on the day it
      publishes, since both are built with the same date, and the blog build fails if a guide
      links a post it did not publish.
- [x] **Each school page links to the posts that quote it.** Eleven MBA posts link to 54
      school pages where they quote the schools' figures, and no school page linked a post
      back. A school page now shows "In the Study Room": up to five published posts that link
      it, newest first. None is published yet, so no page shows the section today; the first
      appear on October 28 with the tuition post, and a build dated November 21 shows it on
      all 54. The blog build's check that every link into the blog is a published post now
      covers the school pages too.
- [x] **"How Much Does the ACT Cost in 2026?" queued for November 23**, James Corbett,
      completing the fee posts for all five live exams: ACT's fees in the United States ($70,
      $75 with science, $95 with writing, $100 with both) and outside it ($188.50 to
      $223.50), every other fee (late registration $42, the $49 change fee, standby $75,
      score reports $20, the $32 archive fee, My Answer Key and score verification), what
      missing a test costs, the few refunds ACT gives, and the fee waiver's benefits, rules
      and eligibility. The ACT guide gains six key facts from ACT's US and non-US fees pages,
      its registration, score sending and fee waiver pages and its 2026-2027 fee waiver PDF,
      checked weekly (108 exam facts against 67 pages, none missing). ACT's registration page
      says My Answer Key is offered on three test dates a year and its fee waiver page says
      four, so the post says only that it is offered on some dates.
- [x] **The fonts are served from this site** (INC-0163, DEVSECOPS O6 closed as F6). Every
      page fetched its fonts from Google, so first paint waited on two Google hosts and each
      visit told Google who came, and each of 30 page sources asked for its own weights: the
      shared header's 700 weight drew as 600 on the 25 that stopped at 600. The three faces
      now come from `/vendor/fonts-2026-09-27/` (52 faces in 28 files, Google's own files,
      with their licenses), through one stylesheet every page links via `{{FONTS_CSS}}`; the
      CSP no longer allows Google's font hosts; the trainers precache the fonts for offline
      use; and both builds fail on a font or stylesheet from another host, or one of ours
      that is missing. The header's Create Account label now measures 93.61px on each page
      measured (the landing page, /exams/, /daily/, /blog/ and the terms page), where it
      was 92.41px on the landing page and /exams/.
- [x] **The community page no longer slides sideways on phones** (INC-0164). The line
      naming a signed-out visitor's pseudonym could not wrap, so a long random name, up to
      Crimson Kingfisher 98, pushed the page 35px past a 390px screen. The line now wraps
      with the name kept whole, and `src/smoke_community.js`, in the browser suite, checks
      the longest and shortest names the page can draw at phone and desktop width.
- [x] **Two more acceptance rates, and an estimate is called one** (INC-0167). Acceptance
      rate is the largest search intent on the school pages, and the library had one in 15
      of its 94 school records. Scanning every page the library already cites found two more:
      Columbia's 19.5%, which Poets&Quants marks as an estimate from CBS data, and Maryland
      Smith's 38% on the Poets&Quants profile its women and international shares come from.
      Both were re-read live on September 27 and pass the source check (653 figures, none
      missing). The school pages called every rate "reported", so Harvard's 11.3%, which its
      source describes as estimated, read as reported too; the lead, profile sentence, meta
      description and FAQ now say "estimated" wherever the figure's own source does, and the
      build fails a page that calls an estimate reported. The SFN Score counts acceptance
      rate at 10 percent where one exists: Columbia moves from 93.0 to 91.2 and stays 5th,
      Maryland from 58.9 (42nd) to 56.7 (45th), and Utah, SMU and Michigan State each move up
      one place.
- [x] **Five more long reading passages** (flooding in a lead mine, buried coin hoards,
      earthquake damage in a market town, a valley's changing birdsong, crumbling book
      bindings), invented like the rest of the corpus, each a revision narrative with its two
      rules printed, 317 to 334 words, with no researcher or place another passage uses. The
      banks grow by 50 GMAT, 50 GRE and 50 LSAT items (GMAT 34162, GRE 20538, LSAT 14442 of
      which 14070 are generated), and llms.txt and the EDITORIAL product facts carry the new
      counts. Every item from the new passages was read at GMAT, GRE and LSAT length. Two
      first drafts were replaced because short passages already covered their ground
      (orchard pollination, and bakers and bread prices), and the build refused one near
      miss (INC-0169): the corpus check counted "no water was pumped" as negative, and the
      builder, which capitalises first, did not. Negatives now match in any case.
- [x] **A live post's wrong GMAT retake rule, and Title Case on every post heading**
      (INC-0170, INC-0171). "Should You Retake the GMAT?", live since August 25, said GMAC
      limits attempts across a lifetime; GMAC's retake policy page, read on September 27,
      sets at least 16 days between attempts and five in a rolling 12 months and names no
      lifetime limit. The post and its FAQ now give those figures and link the policy page,
      and the blog build keeps a table of retired claims that fails any post repeating one.
      The same post's headings were sentence case, like those of the 30 posts published
      from August 17 to September 20: 204 headings across 32 posts now follow the house Title
      Case rule, and the blog build fails a heading that breaks it.
- [x] **The ACT has no attempt limit** (INC-0172). The ACT exam guide, the live SAT vs ACT
      post and the queued ACT format guide said the ACT can be taken up to 12 times; ACT's
      retesting page, which the record cites, now says there is no limit and that students
      take it 2 to 3 times on average to reach their goals. The weekly source check had passed
      the 12 because the page's "K-12" menu link prints it; grade ranges no longer count as
      figures there, and the retired-claims table refuses a 12-attempt ACT cap in any post.
      ACT's retesting page also says fee waivers cover up to four tests where its fee waiver
      page and requirements say two; posts follow the program page (EDITORIAL.md).
- [x] **Exam figures confirmed by numbers that meant something else** (INC-0173 to
      INC-0175). An audit of every exam figure the source check found only away from all of
      the fact's words turned up 21 numbers: 18 were percentile table cells, confirmed row by
      row, and three were wrong confirmations. The GMAT's five-year score validity cited
      GMAC's retake article, where "up to 5 times" supplied the 5; it now cites GMAC's
      validity article, which says scores are valid for five years and reportable for up to
      10. The GMAT score release said "3 to 5 days" with an email notification; GMAC's article,
      updated September 9, says within five days, up to 20 though not typically, and that
      scores cannot be expedited, and the 3 had come from its "0 out of 3 found this helpful"
      counter. GRE's five-year validity cited ETS's scores overview, which never states it:
      the check's tag pattern ended a tag at a > inside a quoted attribute, and an element
      id's 5 leaked into the text. It now cites ETS's Get Your Scores page ("reportable for 5
      years following your test date"), and the live GRE format guide says so in place of
      "a multi year window". The check now reads markup with an HTML parser, wants each
      exam figure beside one of its fact's words or in a table, recognises Imperva's
      script-only challenge, and caches no read too short to be evidence. All 108 exam facts
      pass: 106 in the run of September 27, and the two on GMAC's policies PDF against a
      direct read the same day, since Imperva challenged the run's reads of it.
- [x] **Five more long reading passages** (bells, saltwells, schooldays, canal, wrecks):
      church bells whose cracking was blamed on hard winters, cracked by a new supplier's
      impure tin; town wells whose salt was blamed on sea floods, drawn in by a brewery's
      pumping; school absences blamed on the harvest, caused by flooded fords; a canal's lost
      trade blamed on the railway, lost to a leaking reservoir; and shipwrecks blamed on
      wreckers, caused by a chart that placed a sandbank too far out. The first drafts of two
      were replaced before commit: a saltmarsh starved of silt repeated the short corpus's
      saltmarsh passage, and a honey passage would have made a third about bees. Every name
      was checked against every corpus and bank, and the places are invented rather than
      real towns. They run 290 to 309 words and pass the premise, answer tell and key spread
      checks. The banks grow by 50 GMAT, 50 GRE and 50 LSAT items: GMAT 34262, GRE 20638 and
      LSAT 14542, of which 14170 are generated, counts read from the build. All 150 new items
      were read at LSAT, GMAT and GRE length; one ambiguity was fixed first ("they fell in
      the weeks of winter flood" became "they were clustered in").
- [x] **Five more long reading passages** (lending, chimneys, coaches, bakehouses,
      pieces): falling loans at a subscription library blamed on cheap newspapers, caused by
      lending hours that clashed with mill shifts; chimney fires blamed on careless servants,
      caused by a licence fee that drove out the sweeps; late coaches blamed on a rutted road,
      caused by a post office order to wait for the mail; bread shortages blamed on hoarding
      millers, caused by a ban on cutting furze for the bakers' ovens; and weavers' falling
      earnings blamed on power looms, caused by merchants lengthening the piece at the same
      rate. Every name was checked against every corpus and bank (two first choices were
      taken and replaced), and the places are invented. They run 292 to 309 words and pass
      the premise, answer tell and key spread checks; the premise check first asked for a
      negatively worded near miss in two rules, so the key would not be the only negative.
      The banks grow by 50 GMAT, 50 GRE and 50 LSAT items: GMAT 34312, GRE 20688 and LSAT
      14592, of which 14220 are generated, counts read from the build. All 150 new items were
      read, and each has exactly one key.
- [x] **"Do You Get a Break During the GMAT, GRE, LSAT, SAT, or ACT?"** queued for December
      17 (Maya Chen): the GMAT's optional 10-minute break after the first or second section,
      none on the GRE, the LSAT's full 10-minute intermission after Section 2, the SAT's 10
      minutes between its sections, and the ACT's short break after its second test. Every
      rule was read on September 28; five join data/exams.json and pass the source check
      against their live pages, and EDITORIAL.md gains a breaks block.
- [x] **The weekly source check's issue #182, resolved** (INC-0182, INC-0183). Of the five
      school figures it reported, three were Arizona State W. P. Carey's: on September 28
      its class profile replaced the figures under its unchanged "Incoming class of Fall
      2025" heading, and the library now has 24 percent admitted, an entering class of 45,
      6.2 years, 33 percent international and, since the page now names the edition, a GMAT
      Focus average of 645. The old class size of 47 had passed only because the check read
      the page's "Business 47%", under the heading "Class composition", as the head count; a
      percentage no longer confirms a count, a score or a length of time. Berkeley Haas's
      $92,755 and Buffalo's $16,655 and $7,615 were right all along: both sit in collapsed
      accordions, which the browser read left out whenever a site refused the plain read, as
      these did on GitHub's runner. It now also reads the panels a page's own controls open
      and closed details elements, outside navigation. Three unpublished November posts that
      repeated ASU's figures were corrected: work experience (the range now ends at 6.2 years
      at ASU, and 27 of 37 sit between 4.9 and 6), international share (33 percent) and GMAT
      (ASU added at 645, now 26 programs, half at 670 or higher). With both changes the school
      run of September 28 reads 654 figures against 242 sources with none missing from its
      page, and the exam run 128 facts with none missing; 15 and 2 sources were unreadable
      from this sandbox, to bot challenges, certificate errors and dropped connections.
- [x] **The 14 school figures worth reading, read and recorded.** The school run listed 14
      figures found beside their labels only near another program's name, and every one was
      read on its page as this program's figure: Tepper's class size and international share
      under its Full-Time MBA Class of 2027 (the Hybrid MBA is a side menu link), Fordham's
      two in its "MBA program specific facts" block (the EMBA and MS names are ranking lines
      above it), Howard's 2020 placement, Rutgers' Full-Time MBA FAQ answer, Temple's Full-Time
      MBA Class of 2023 placement, Tennessee's full-time MBA placement, and San Diego's four in
      the Full-Time MBA column of its comparison chart. A list a person has judged stops being
      read if it repeats every week, so data/source_triage.json now takes an entry with `near`,
      the program names the check found, and the check lists such a figure with the triaged
      ones while its value and those names stay the same. A changed figure, or a program newly
      named beside it, is reported again, and validate_schools refuses an entry whose figure
      has changed.
- [x] **"Can You Get Extra Time on the GMAT, GRE, LSAT, SAT, or ACT?"** queued for
      December 19 (Sarah Whitfield): how each test maker takes accommodation requests and how
      long review takes. GMAC aims to respond within 16 to 20 business days and will not add
      accommodations to an appointment already booked; ETS's page says about 6 weeks and its
      2026-27 Supplement four to six, both before scheduling; LSAC takes requests only from
      registered test takers and only until the registration deadline; College Board says up
      to seven weeks; and ACT, since June 2026, closes requests at the registration deadline.
      GMAC's old accommodations URL now says the page has moved, so the post cites its current
      page and help center articles, which answer the source check's user agent. Every rule
      was read on September 28; nine join data/exams.json and pass the source check's
      functions against their live pages, and EDITORIAL.md gains an accommodations block.
- [x] **Bloomberg's 2026-27 edition, caught** (INC-0184). A school run read Bloomberg's
      Vanderbilt page as a page for once, rather than its bot challenge, and found the 2026-27
      profile: No. 17 in the US and a median base salary of $142,800, where the library held
      the 2025-26 edition's rank of 27 and $150,000. Vanderbilt's salary moves to $142,800.
      The check now reads every rank whose edition is written like 2025-26 and fails on one
      whose page names a later edition, since a rank has no `v` and had never been read; its
      first run flagged 29 Bloomberg ranks, every one a real 2025-26 rank on a page now
      naming 2026-27, and nothing else.
- [x] **Bloomberg ranks moved to the 2026-27 edition.** Bloomberg's US ranking page first
      answered this sandbox with an "Are you a robot?" challenge (the owner was told at once),
      then served the page to the source check's next read, with all 66 schools. From that
      read, 40 ranks move to 2026-27 (Texas A&M up from 41 to 22, Vanderbilt from 27 to 17,
      Berkeley Haas down from 3 to 8, Georgetown from 22 to 31), 22 schools in the library gain
      a Bloomberg rank for the first time (among them Maryland at 25, Georgia Tech at 26 and
      Washington University in St. Louis at 40), and Penn State and UC San Diego, absent from
      the 2026-27 list, no longer carry one. Every entry now cites Bloomberg's own ranking
      page rather than a school press release or a news summary.
- [x] **Every rank names its edition** (INC-0185). The two ranks with no edition were both
      Financial Times: Penn State's 47 came from a Spring 2021 magazine article, and Maryland's
      31 was an older edition's US position, where every other FT rank in the library is a
      position worldwide. Neither school is among the 100 in FT's 2026 table, so both are now
      blank for the 2026 edition, and validate_schools refuses a rank that names no edition or
      has no source url. Cornell's, UCLA's and Washington Foster's FT ranks now cite
      Poets&Quants' report of the 2026 ranking instead of two admissions consulting blogs.
- [x] **"What Should You Bring to the GMAT, GRE, LSAT, SAT, or ACT?"** queued for December 21
      (Elena Rodriguez): what each test center requires, allows and keeps out, and when to
      arrive. GMAC allows no food or drink without an accommodation and asks you to arrive at
      least 30 minutes early; ETS allows only your ID and a mask in the GRE testing room; LSAC
      puts phones, food and beverages in lockers and asks you to arrive up to 30 minutes early
      with your LawHub login memorized; College Board wants a charged device with Bluebook set
      up and lets you bring a drink or snacks for the break; ACT wants No. 2 pencils and you
      inside by 8:00 a.m. Every rule was read on September 28 from the test makers' own test
      day pages; five join data/exams.json and pass the source check's functions against their
      live pages, and EDITORIAL.md gains a test day block.
- [x] **"Can Schools See All Your GMAT, GRE, LSAT, SAT, or ACT Scores?"** queued for December
      23 (Aisha Thompson): which scores each school receives and where the choice ends. LSAC
      reports every LSAT result from the current testing year and the five before it,
      cancellations and absences included; ETS's ScoreSelect, College Board's Score Choice and
      ACT's reports by test event let you choose, though ETS and College Board say some
      programs want every score; and a GMAT report now carries the GMAT Superscore, with the
      best section scores of other attempts and their dates, which cannot be left off. Every
      rule was read on September 28 from the test makers' own pages; four join
      data/exams.json and pass the source check's functions against their live pages, and
      EDITORIAL.md gains a block on what schools see.
- [x] **"How Late Can You Register for the GMAT, GRE, LSAT, SAT, or ACT?"** queued for
      December 25 (David Okafor): GMAC sets no deadline, with test centers open throughout
      the year and online appointments 24/7 in many regions; ETS asks two calendar days'
      notice online and two business days by phone; the LSAT has one deadline per
      administration (the February 2027 LSAT closes December 29, 2026); and the SAT and the ACT
      add paid late windows ($38 and $42) after their deadlines. Every rule was read on
      September 28; the GMAT and GRE rules join data/exams.json and pass the source check's
      functions, the 2027 dates come from data/test_dates.json, which test_dates.py confirmed
      in step with all three makers that day, and EDITORIAL.md gains a registration block.
- [x] **The live retake post explains the GMAT Superscore.** "Should You Retake the GMAT? A
      Decision Framework" (published August 25) gains a section on the Superscore GMAC launched
      on August 12, 2026: best section scores across attempts, sent automatically with every
      single attempt score and impossible to leave off, and in GMAC's own advice no reason to
      take an attempt less seriously, since schools see that single attempt score too. Its FAQ
      line that "most programs say they consider your best score" had no source; it now says
      what GMAC shows a program and that each school sets its own policy. MIT Sloan's figure
      moves to the Class of 2028 profile (median 675, middle 80 percent 645 to 715, read on
      MIT's page September 28), the retake policy cites GMAC's current article, and three
      Superscore facts join data/exams.json after passing the source check's functions.
- [x] **"Free Official GMAT, GRE, LSAT, SAT, and ACT Practice Tests"** queued for December 27
      (James Corbett): what each test maker gives away. GMAC's free Official Starter Kit has
      Practice Exams 1 and 2, adaptive and scored like the exam but without answer
      explanations; ETS offers POWERPREP Online 1 (untimed, so no Verbal or Quant scores) and 2
      (timed), with POWERPREP PLUS at $44.95 a test; LSAC puts four full PrepTests on LawHub,
      with LawHub Advantage at $124 a year; College Board's full-length SAT tests are free and
      scored in Bluebook, and as nonadaptive PDFs; and ACT offers Practice Tests 1 to 4, digital
      or paper, always free. Every rule was read on September 28 from the makers' own pages;
      six join data/exams.json and pass the source check's functions against their live pages,
      and EDITORIAL.md gains a practice tests block. The GMAT facts cite GMAC's help center,
      because mba.com's Starter Kit page served Imperva's CAPTCHA on some reads.
- [x] **"What Happens If You Miss the GMAT, GRE, LSAT, SAT, or ACT?"** queued for December 29
      (Maya Chen): each test maker's rule for a missed appointment. A missed GMAT is a No Show,
      with the fee forfeited, a 24-hour wait to book again and a new fee, though it costs no
      attempt; a missed GRE forfeits the fee, but institutions hear nothing of it, and more than
      12 minutes late at home cancels the test; an LSAT absence is reported to law schools
      unless you withdraw by 11:59 p.m. ET the night before; College Board offers makeup SATs
      for closed centers and misadministrations; and ACT lets a missed test move to a later
      date for the $49 change fee. Every rule was read on September 28 from the makers' own
      pages; five join data/exams.json and pass the source check's functions, and EDITORIAL.md
      gains a missed test block.
- [x] **Five more long reading passages** (eelweirs, silting, honeyfields, thatch, flaxretting):
      eel catches falling on a river, blamed on the net men and caused by new weirs too high for
      the young eels to climb; a harbour silting up, blamed on great storms and caused by walled
      salt marshes that no longer sent the tide out to scour the channel; honey yields halving,
      blamed on cold springs and caused by farmers ploughing in the clover and buckwheat the
      bees fed on; thatched roofs failing early, blamed on wet summers and caused by threshing
      machines that bruised and broke the straw; and linen growing weak, blamed on foreign seed
      and caused by a court order that sent flax from the river to rot unevenly on the grass.
      They run 290 to 310 words, every name was checked against every corpus and bank, and they
      pass the premise, answer tell, key spread, covers and stem checks. The banks grow to
      GMAT 34412, GRE 20788 and LSAT 14692, of which 14320 are generated, counts read from the
      build. Reading the items first changed two wrong answers that a careful reader could have
      defended: "the hive at Furze End stood on the heath" and "the piece bought from the
      Dunnock farm was steeped in a pond" name the one alternative the passage gives, so each
      could look inferable, and each now contradicts the study instead, as earlier passages' do.
- [x] **Five more long reading passages** (shiptimber, leadroofs, oysterbeds, bridgetolls,
      fullersearth): warships rotting early, blamed on careless shipwrights and caused by a
      forest felling its oak in summer so the bark could be sold to the tanners; church roofs
      cracking, blamed on hard winters and caused by plumbers casting thinner lead after its
      price rose; oyster beds dying, blamed on a hard winter and caused by sand from a new
      ballast ground; bridge tolls halving, blamed on hard times and caused by a turnpike road
      that sent the carriers round by a ford; and cloth failing the searchers, blamed on the
      weavers and caused by gritty fuller's earth from a new pit. They run 302 to 346 words,
      every name was checked against every corpus and bank, and they pass every check the bank
      build runs. The banks grow to GMAT 34462, GRE 20838 and LSAT 14742, of which 14370 are
      generated, counts read from the build. All 150 new items were read before they went in.
      Two near misses were rewritten first, because each named what the passage's own
      alternative implied: a lot of oak missing from the forest's accounts "was not felled in
      summer" (it might be the winter-felled estate oak), and a mill that never bought its
      earth "did not use the earth from the new pit" (it might be the mill that dug its own).
- [x] **Five more long reading passages** (brickfields, herringcure, warrens, tallow,
      charcoaliron): bricks crumbling in a town's new terraces, blamed on hasty builders and
      caused by clay from a pit full of lime; cured herring spoiling, blamed on the coopers and
      caused by damp salt from a new works; rabbit warrens failing, blamed on poachers and caused
      by the enclosure of the heath's gorse; candles guttering, blamed on cheap wick and caused
      by soft tallow from cattle fed on oilcake; and iron turning brittle, blamed on a new bed of
      ore and caused by charcoal burned from green wood. They run 316 to 346 words, every name
      was checked against every corpus and bank, and they pass every check the bank build runs.
      The banks grow to GMAT 34512, GRE 20888 and LSAT 14792, of which 14420 are generated,
      counts read from the build. All 150 new items were read before they went in, and the near
      misses were written from the start to avoid the passage's own alternative (the gorse left
      standing, the grass-fed tallow, the seasoned wood), the trap the last two batches found.
- [x] **Five more long reading passages** (clockdials, vatwater, seasand, brewyeast,
      slatenails): church clocks stopping on winter nights, blamed on a new clockmaker and caused
      by ice on the iron hands of new outside dials; paper spotting, blamed on a new rag merchant
      and caused by vat water from a leat that carried rust; a pier's mortar crumbling, blamed on
      the masons' haste and caused by salty sand dug from the beach; ale souring, blamed on a new
      maltster and caused by yeast bought from one common brewer; and slates slipping, blamed on a
      new quarry's thin slate and caused by iron nails that rusted through. They run 325 to 344
      words, every name was checked against every corpus and bank, and they pass every check the
      bank build runs. The banks grow to GMAT 34562, GRE 20938 and LSAT 14902, of which 14530 are
      generated, counts read from the build. All 150 new items were read before they went in, and
      the reading changed three things first. The clock passage had blamed rape oil thickening in
      the cold, the street lamps passage's cause, and the two met as main idea choices, so it now
      blames ice on new outside dials. A case at Scarth Chapel met a researcher named Scarth, and a
      stationer named Ezra met the thatcher Ezra Merriott, so both were renamed, with two inns whose
      names other generators use. And "clocks he had never touched" named no one when its sentence
      was quoted alone as an answer choice.
- [x] **Five more long reading passages** (rickfires, wallrender, butterchurns, blastpowder,
      frostoaks): hay ricks catching fire, blamed on rick burners and caused by hay carried to the
      rick before it had dried; medieval wall paintings flaking, blamed on a restorer's paint and
      caused by cement render that held the damp in the walls; butter turning rank, blamed on
      careless dairymaids and caused by churns lined with copper; blasting charges misfiring,
      blamed on a new powder mill and caused by powder that drew damp in a new magazine; and young
      oaks dying, blamed on the deer and caused by seedlings raised in a mild climate and killed by
      late frosts. They run 316 to 345 words, every capitalised word was checked against every
      corpus and bank, and they pass every check the bank build runs. The banks grow to GMAT
      34612, GRE 20988 and LSAT 14952, of which 14580 are generated, counts read from the build.
      All 150 new items were read before they went in. Five names met names already in use
      (Ashcombe, Brackwater, Kestrel, Penhallow and Winstanley) and were changed; the rick
      passage's second study moved from a fire office's claims to a land agent's rick books,
      because its caveat about uninsured ricks sat too close to the chimney fires passage's caveat
      about uninsured houses, which can be drawn as a wrong answer beside it; and the wall painting
      passage's surveyor became an antiquarian society, for the same reason against the brickfields
      passage's surveyor who had no duty to inspect.
- [x] **The error beacon reports only from visitors' pages, once per page** (INC-0196,
      INC-0197): client_errors held five rows from a smoke test that had opened a built page from
      disk, posted by the beacon as if a visitor had hit them, and 12 smoke scripts open pages with
      no request interception, so any error a test run catches would reach the live table. The
      beacon now stays silent under automation (navigator.webdriver) and on pages opened from
      disk, and build.py runs its script in node in all three contexts. Reading the table also
      found every blog page carrying the beacon twice, because the blog builder appended its own
      after a footer that already carries one; three blog page loads left identical pairs. The
      blog's copy is gone, and both builds now require exactly one beacon on every page they
      write. The five test rows stay in the table for the owner to mark as noise in Admin > Errors.
- [x] **Five more long reading passages** (redwater, footrot, grittyflour, fadedink,
      troutgravel): cattle sickening with redwater, blamed on a new breed and caused by ticks
      multiplying in bracken the commoners were no longer let cut; ewes going lame, blamed on a new
      breed of ram and caused by folding them on water meadows floated longer each spring; flour
      turning gritty, blamed on the millers' haste and caused by millstones cut from a soft
      sandstone; registry entries fading, blamed on the clerks' thrift and caused by a new
      stationer's logwood ink; and trout declining, blamed on poachers and caused by silt from new
      cress beds smothering their spawning gravel. They run 308 to 329 words, every capitalised
      word was checked against every corpus and bank, and they pass every check the bank build
      runs. The banks grow to GMAT 34662, GRE 21038 and LSAT 15002, of which 14630 are generated,
      counts read from the build. All 150 new items were read before they went in. A case name
      that met the salt wells passage's Tanner's Row became Pinfold Croft, and the flour passage
      changed once the items were read: it limited its second study to members of the bakers'
      company, which made the bread shortages passage's closing limit, "less is known about the
      town's other bakers", half true of it when drawn as a wrong answer beside it. Every baker who
      bought from the mills now belongs to the company, and the limit names only the meal ground
      for households.
- [x] **The October 3 Search Console export, read against September 26** (INC-0198): the
      surge of September 21 to 25 (1,412 to 1,699 impressions a day at deep positions) settled
      back to 618 and 662 a day by September 28 and 29, close to early September, but higher:
      the five new days averaged position 26.9, and school page impressions in them averaged 15
      against 34 before. GROWTH.md records it. The queries near page one ask what the pages
      already answer, so the lever is still links from other sites. The report tool gained
      `--since`, which reports only the days a later export adds, since exports are
      overlapping windows; it subtracts by page type, where the Pages sheet lists 99 percent of
      impressions, and says why it does not by intent, where the Queries sheet lists 36 to 41
      percent. It no longer tells us to redirect the retired MCAT and Executive Assessment
      guides, which the Worker has redirected since INC-0109, and it counts queries written in
      search-operator syntax on their own line, out of the striking-distance list.
- [x] **GRE sentence-function questions no longer offer a second right answer** (INC-0199):
      one wording of the third sentence's job, "present a finding that tells against the
      earlier account", is also true of the fourth sentence, the second finding, and 31 of the
      107 fourth-sentence questions offered it as a wrong answer (34 second-sentence questions
      offered it too, where it is arguable). It now reads "present the first of the two
      findings that tell against the earlier account", and the build fails unless every
      wording for either finding says which finding it is, the one thing that tells them
      apart. Found while reading the schema as the model for generated LSAT structure
      questions.
- [x] **Generated LSAT structure questions** (Meaning, Structure and Tone): the category
      had only its 20 hand written items. A new schema over the long passages quotes a part of
      the passage, the way LSAT stems do ("The author's statement that ... serves primarily
      to"), and asks what it does there: the grounds for the earlier account, what that account
      could not explain before any study, the first finding, the second, or the closing limit.
      Every passage has those parts in that order, so each answer is fixed by the passage's
      structure, and the wrong answers are the other parts' jobs, each worded to be false of
      every part but its own (INC-0199). The record notes are not asked, because in the older
      passages some describe records and some rule out a rival cause, and no one job is true of
      all of them. What the account could not explain is quoted from after "The account could
      not explain why", so the stem does not name its job, and asked only of the 76 of 89
      passages whose sentence has that form; one closing limit opens "That" and would print
      "that that", so it is skipped. 431 questions, and the build checks that every quote
      appears in the passage as printed. The LSAT bank grows to 15433, of which 15061 are
      generated; the author's attitude stays hand written.
- [x] **Five long reading passages on new ground** (lasttram, filmstore, horsesetts,
      smokerickets, cableduct): the last ten batches were all rural trades, so these move to
      the town and the twentieth century. A theatre's dwindling audiences, blamed on the first
      cinema and caused by a tram company running its last car before the curtain fell;
      newspaper microfilm turning brittle and sour, blamed on readers and caused by a warm,
      damp basement store; omnibus horses going lame, blamed on a contract farrier and caused
      by smooth granite setts on the steep streets; rickets, blamed on mothers' cooking and
      caused by smoke from a new works cutting off the sunlight children's skin needs; and
      telephone calls failing in wet weather, blamed on new operators and caused by water in a
      cable duct laid below the water table. They run 317 to 325 words and each adds ten items
      to GMAT, GRE and LSAT and five LSAT structure questions: the banks grow to GMAT 34712,
      GRE 21088 and LSAT 15508, of which 15136 are generated, counts read from the build. All
      the new items were read before they went in. Four names met names already in use
      (Fenwick, Thornleigh, the Courier and Bridge Street) and were changed, and two sentences
      were reworded: gallery seats that cost no more than "the cinema" now cost no more than a
      seat at it, and "cable insulated with paper that takes in water" left it unclear what
      took in the water.
- [x] **School pages say a figure the way the school does** (INC-0200): eight pages stated
      a class size as one class's exact count ("a class of 41", "has 41 students") where the
      school gives an average cohort size (George Washington, Michigan State, Minnesota, Rice),
      a typical cohort (Olin) or an approximate size (Louisville, Ohio State, Oklahoma). UC
      Riverside's tuition lost the school's "approximately", Lehigh's work experience its
      "more than", and the list's scholarship notes for Harvard and Stanford their
      "approximately" and "roughly". One reader now takes the qualifier from each figure's own
      note, the old one knew a single word and served program cost alone, and an averaged
      cohort size is its own sentence ("Mendoza College of Business cohorts average 85
      students"). The build fails if a page states a qualified class size without its
      qualifier, or if a note carries a qualifier no sentence can word yet. Notre Dame's class
      size is filled from Mendoza's MBA page, read October 5: an average cohort of 85. The
      page also prints a 655 median GMAT, which stays out, because it names no edition
      (INC-0157).
- [x] **Five more long reading passages on new ground** (boilerscale, streetlamps,
      softwater, hedgethorns, dampflats), again away from the rural trades:
      - Railway boiler tubes bursting, blamed on firemen chasing a bonus and caused by hard
        water from a new well.
      - Market garden spinach running to seed, blamed on the seedsman and caused by new
        electric street lamps that left the beds no long night.
      - Lead poisoning, blamed on cheap glazed crocks and caused by soft, peaty reservoir
        water that ate into the lead pipes.
      - Bicycle punctures on country lanes, blamed on a shop's tyres and caused by new
        flail hedge cutters strewing thorns.
      - Mould in new council flats, blamed on tenants drying washing indoors and caused by
        blocks built without the flues whose draught carried the moisture away.

      They run 325 to 344 words and each adds ten items to GMAT and GRE and fifteen to
      LSAT. The banks grow to GMAT 34762, GRE 21138 and LSAT 15583, of which 15211 are
      generated; the counts were read from the build. Every new item was read before it
      went in, with three changes:
      - The first draft of the main idea lines echoed the passages word for word and
        tripped the word-matching guard (INC-0117) at 40.4 percent against a 40 percent
        ceiling. They now paraphrase ("a run of flat tyres put down to a shop's poor stock
        was mainly the work of a new way of cutting hedges").
      - Six names were changed because they shared a stem with names already in use:
        Harrop beside Harrow, Ravensike beside Ravenstone, Easterhope beside Easterlow,
        Sallowdale beside Sallowmere, Ferrier beside Ferris, and Tolley, a letter away
        from the Tolly mound, which other passages' questions can print beside it.
      - One sentence said "clippings" twice.
- [x] **"What's on Your GMAT, GRE, LSAT, SAT, or ACT Score Report?"** queued for December 31
      (Sarah Whitfield): what each report shows and what schools receive. GMAC's report adds
      percentile rankings, performance insights and the Superscore, with no PDF version; ETS's
      Institution Score Report carries only the scores you choose and no sign of other GRE
      tests, though schools can see your photos and essays; LSAC's lists up to 12 reportable
      results with a percentile rank for each and a score band; College Board's adds a Score
      Range and eight content areas; and ACT's adds STEM, ELA and reporting categories. Every
      rule was read on September 28 from the makers' own pages; seven join data/exams.json and
      pass the source check's functions, and EDITORIAL.md gains a score report block.
- [x] **"What Math Is on the GMAT, GRE, SAT, and ACT?"** queued for January 2 (Aisha
      Thompson): what each test's math covers, in its maker's words. The GMAT's Quantitative
      Reasoning is algebra and arithmetic with no calculator; the GRE's four content areas stop
      at a second course in algebra, with no trigonometry or calculus; the SAT weights Algebra
      and Advanced Math at about 35% each and Problem-Solving and Data Analysis and Geometry and
      Trigonometry at about 15% each; and the ACT reports Preparing for Higher Math at 80% and
      Integrating Essential Skills at 20%. Every rule was read on September 28 from the makers'
      own pages; four join data/exams.json and pass the source check's functions, and
      EDITORIAL.md gains a math block.
- [x] **"What Verbal Skills Do the GMAT, GRE, LSAT, SAT, and ACT Test?"** queued for January 4
      (David Okafor): the verbal side of each test, in its maker's words. The GMAT's Verbal
      Reasoning is Reading Comprehension and Critical Reasoning; the GRE gives about half its
      verbal measure to completing sentences and paragraphs; the LSAT gives two of its three
      scored sections to Logical Reasoning; and the SAT and the ACT publish the share of each
      reading and writing domain, grammar included. Every rule was read on September 28 from
      the makers' own pages; three join data/exams.json and pass the source check's functions,
      and EDITORIAL.md gains a verbal block.
- [x] **"Does the GMAT, GRE, LSAT, SAT, or ACT Have an Essay?"** queued for January 6 (James
      Corbett): only the GRE scores an essay at every sitting, an Analyze an Issue task in 30
      minutes; the LSAT requires an unscored Argumentative Writing sample, 15 minutes of
      prewriting and 35 to write, before scores are released; the ACT's 40-minute essay is
      optional; the SAT's Essay survives only on school days in states that require it; and the
      GMAT Focus Edition has none. Every rule was read on September 28 from the makers' own
      pages; three join data/exams.json and pass the source check's functions, and EDITORIAL.md
      gains an essay block.
- [x] **"Should You Guess on the GMAT, GRE, LSAT, SAT, or ACT?"** queued for January 8 (Maya
      Chen): LSAC and ACT deduct nothing for a wrong answer, ETS's GRE scoring counts the
      questions answered correctly, College Board says a guess beats a blank for most students,
      and GMAC counts the number of questions answered as one of three factors in each GMAT
      section score. It also covers what each test lets you do with a question you mean to
      return to, from the GMAT's three changed answers to the SAT's module you cannot go back
      to. Every rule was read on September 29 from the makers' own pages; six join
      data/exams.json and pass the source check's functions, and EDITORIAL.md gains a guessing
      block.
- [x] **"How Adaptive Testing Works on the GMAT, GRE, and SAT"** queued for January 10 (Sarah
      Whitfield): the GMAT adapts question by question from a medium-difficulty start, the GRE
      sets its second Verbal and Quantitative sections by the first, and the SAT sets its second
      module in each section by the first, with what each design lets you go back to. The LSAT
      and ACT are left out because neither maker's pages describe their test as adaptive. Every
      rule was read on September 29 from the makers' own pages; three join data/exams.json and
      pass the source check's functions, and EDITORIAL.md gains an adaptive testing block.
- [x] **"What If Something Goes Wrong on the GMAT, GRE, LSAT, SAT, or ACT?"** queued for January 12
      (Elena Rodriguez): what each test maker offers when a technical problem or disruption hits a
      test, and what to do on the day. GMAC's Testing Issue remedies and seven-day reporting window,
      ETS's free retest or refund and travel claim, LSAC's remote pause and resume, College Board's
      Help icon and makeup tests, and ACT's discretionary retest or refund. GMAC's policies PDF
      answered with a bot challenge earlier on September 29 and served the PDF again the same day;
      the source check's own client is still challenged, so the two GMAT facts were checked, with
      the source check's functions, against a plain download of the same PDF. Six rules join
      data/exams.json, and EDITORIAL.md gains a test day problems block.
- [x] **No rank cites an admissions consulting blog.** Eight U.S. News 2026 ranks (Virginia
      11, Cornell 15, UCLA and Texas 18, Washington 20, North Carolina 21, Emory 23, Georgetown
      31) cited Clear Admit or Stacy Blackman, which src/sources.py lists as weak sources; they
      now cite Poets&Quants' table of the ranking, sourced to U.S. News, which gives the same
      ranks and ties. Emory's Financial Times 56 now cites the FT's own 2026 table, whose Rank in
      2026 column gives 56 and whose Rank in 2025 column gives 45. No value changed.
- [x] **Five more long reading passages** (organs, lamps, ropes, tanpits, hopkilns): church
      organs drifting out of tune each winter, blamed on damp and caused by new stoves; street
      lamps going out before dawn, blamed on idle lamplighters and caused by a cheaper seed oil
      that thickened in the cold; ropes parting at sea, blamed on cheap hemp and caused by a new
      tar kettle that scorched the yarn; leather rotting within a few years, blamed on diseased
      hides and caused by tanners cutting the time in the pits to save scarce bark; and hops
      rejected by the brewers, blamed on a blight and caused by a new coal that tainted them in
      the kilns. They run 289 to 306 words, every name was checked against every corpus and
      bank, and they pass the premise, answer tell, key spread, covers and stem checks. The
      banks grow by 50 GMAT, 50 GRE and 50 LSAT items: GMAT 34362, GRE 20738 and LSAT 14642, of
      which 14270 are generated, counts read from the build. Reading their items found INC-0186
      and INC-0187, and their main idea summaries were reworded before they went in, because
      "ropes parting at sea, blamed on cheap hemp, came mainly from a new tar kettle" reads as
      ropes coming from a kettle.
- [x] **Stated idea questions with two right answers, fixed** (INC-0186). A stated idea
      question offers the passage's other sentences as its wrong answers, which works only
      when the stem picks out one of them. Three of the six stems did not: "in the work of
      Scarth" covers Scarth's finding as well as the note on Scarth's records, and the passage
      joins the second study's finding and its note in one clause, so both of that study's
      asks covered both. 178 of the 378 GMAT and LSAT items on those asks offered the other
      one as a wrong answer. Each ask now records what else its stem is true of and leaves
      those out, the closing caveat included for the two note asks, and the second note ask
      reads "The passage states that, in a later study of ...," instead of "the second set of
      results also established", which called a note on the records a result; its 126
      questions take new ids. g_rc.check_covers builds every ask of every passage and fails
      the build on an ask with no record, or on an item that offers what its record names.
- [x] **The earlier account's difficulty, asked so it reads** (INC-0187). The stated idea
      question about a passage's problem sentence read "the earlier account failed to address
      the fact that", and 49 of the 72 problem sentences name the account itself, so on 143 of
      198 GMAT, LSAT and GRE items the key said the account failed to address the fact that
      the account could not explain something, while a study's finding beside it read as the
      better answer. The ask now reads "According to the passage, even before the studies it
      describes, the earlier account could be faulted because", which every problem sentence
      completes and the studies' findings do not; its 198 questions take new ids.
      g_rc.check_stems renders every stated idea ask with its key on each build and refuses a
      slot that asks for a fact and gets the account itself.
- [x] **What a GMAT score report carries, since the Superscore** (INC-0188). Since August
      12, 2026 every GMAT report sent to a school includes the GMAT Superscore when one
      exists: the best section scores across valid attempts, with the date and delivery
      method of each, and it cannot be left off. Two queued posts said otherwise: the
      December 7 post on free score reports quoted the first sentence of mba.com's paragraph
      ("only ... the exam associated with the score report") and not the next, which adds the
      Superscore, and the December 13 post on canceling told readers schools see only the
      scores you send. Both now say what a report carries and cite GMAC's article on sending
      Superscores; EDITORIAL.md records the Superscore rules, data/exams.json gains two
      Superscore facts for the source check to read, and build_blog refuses the old claim.
- [x] **Watch for notes that named the wrong choices** (INC-0189). Items are written key
      first and their notes with them, so a note's B was the first wrong answer its author
      wrote; bank_emit.permute then shuffled the choices and left the letters behind, and 124
      notes named the correct answer among the wrong ones, from "B is the other objection,
      and C, D and E are not the response described" on an LSAT reading item keyed E to
      "The first option has exactly that form" on a reasoning item keyed E. permute now turns
      {B} style markers into the letter each choice lands on and refuses a bare letter or a
      "second option" left in a shuffled note, and the nine generators write their notes that
      way; the GMAT verbal, quant, ACT and LSAT reading notes no generator reproduces were
      corrected by hand, choice by choice. 200 items' notes changed. test.js now fails any
      note on any exam that names the key among the wrong answers.
- [x] **Four LSAT reasoning items with more than one right answer** (INC-0190, INC-0191),
      found by reading the corrected notes against their choices. LL040's length clause
      supplied the premise that made a wrong answer follow; LL128 offered a second argument of
      the key's form with its terms swapped; LL007 and LL167 offered conditionals the premises
      support. Each now has one right answer and a note that describes its options as they read.
- [x] **Stated questions no longer answered by matching words** (INC-0192). Choosing the
      option with the largest share of its words in the passage found the key on 29 of 44
      hand-written GMAT stated questions, 22 of 30 LSAT, 16 of 25 ACT and 3 of 9 GRE, because
      each key was the passage's own sentence: V261's was "the local position of the sun". The
      68 keys are now said in other words, keeping each one's meaning and its length rank, and
      in the generated banks the rank its lift table sets; V261's is now "the sun as observed from
      that particular town". Two keys that are only a figure stay as they are. The shortcut now
      finds 0 of 44, 0 of 30, 0 of 9 and 2 of 25, and test.js fails any exam where it beats a
      blind guess.
- [x] **Every generated bank is what its generator writes** (INC-0193). The second LSAT
      reading bank was generated on September 21 and corrected in place four times after, so
      by September 28 its script wrote a bank that differed on 25 lines in 23 items, and
      running it would have put back garbled seams, misdirected notes and uneven lengths. The
      bank now says it is edited by hand, the script refuses to write it, and
      src/check_bank_sources.py, run by every build, regenerates the nine banks that name a
      generator and fails on any difference.
- [x] **A repeat with "the" slipped in** (INC-0194). LC041 read "applying the test to
      particular facts to the particular facts in front of them", a seam the exact doubled
      phrase check could not see; it now says it once, and LC036's clause sits where its author
      meant it. test.js and build_banks.py read each text again with a, an and the taken out,
      which finds this item and no other in any bank.
- [x] **"What ID Do You Need for the GMAT, GRE, LSAT, SAT, or ACT?"** queued for December
      15 (James Corbett): GMAC's exact-name and passport rules, ETS's original, signed,
      government-issued ID, LSAC's passport or US or Canadian photo ID that may be up to 3
      months expired, College Board's government or current-school ID with its under-21 and
      abroad rules, and ACT's hard plastic ID or its own form. Every rule was read on
      September 28; five join data/exams.json and pass the source check against their live
      pages (one ACT word was reworded to the page's own). The December 9 calculator post
      now cites GMAC's own calculator and note-taking article, readable since support.mba.com
      answers the source check's user agent: no calculator in Quant or Verbal, personal
      calculators only with the Accommodations team's approval, a booklet and marker at test
      centers and a whiteboard online. That rule joins data/exams.json too.
- [x] **"Can You Cancel Your GMAT, GRE, LSAT, SAT, or ACT Score?"** queued for December
      13 (David Okafor), the post held since the calculator post took its slot. GMAC's own
      article says GMAT scores do not need to be canceled, since you see the official score
      before deciding whether to send it; the GRE's report or cancel choice at the end of the
      test, with reinstatement within 60 days for $50; the LSAT's six calendar days, or six
      days after release with Score Preview, and the Candidate Cancel law schools see; the
      SAT's week after a weekend test; and ACT's cancellation on request from its examinee
      terms. support.mba.com, which refused reads all day, answers requests that carry the
      source check's own declared user agent and refuses those presenting as a browser, so
      its articles are readable after all. Five cancellation rules join data/exams.json and
      pass the source check against their live pages, and EDITORIAL.md gains a canceling
      scores block.
- [x] **"Who Qualifies for a GMAT, GRE, LSAT, SAT, or ACT Fee Waiver?"** queued for
      December 11 (Elena Rodriguez). Who can get each waiver and how to apply, where the
      cost posts cover what each one pays for: GMAT fee waivers, typically distributed
      through business schools and approved programs that decide who is eligible, and
      GMAC's policies on vouchers and fee waivers (the exam fee only, no switching between
      online and test center, never transferred); ETS's four Fee Reduction groups, with the
      $100 General Test against $249; LSAC's two tiers by tax-filing status and income
      against the federal poverty guidelines, with asset and cash limits; College Board's
      six eligibility descriptions and its two routes, a counselor's code or the request
      form, once per lifetime; and ACT's indicators of economic need, decided by a school
      counselor. Every page was read on September 27. support.mba.com refused direct reads
      that afternoon, and the source check's browser read GMAC's article at 18:54 UTC. Four
      eligibility rules join data/exams.json, where the source check reads them weekly, and
      EDITORIAL.md gains a fee waivers block.
- [x] **"Can You Use a Calculator on the GMAT, GRE, LSAT, SAT, and ACT?"** queued for
      December 9 (Sarah Whitfield). The GMAT's on-screen calculator in Data Insights only,
      the GRE's on-screen calculator in Quant, none on the LSAT, and the SAT's and the
      ACT's rules for Desmos and handheld models on math only, with each one's prohibited
      computer algebra models. Every rule was read on September 27; EDITORIAL.md gains a
      calculators block. The post planned for this slot, on cancelling scores, is held:
      GMAC's cancellation article is on support.mba.com, which Cloudflare refused all day,
      and no GMAC page that could be read states the rule. Write it once that page opens.
- [x] **"Free Score Reports on the GMAT, GRE, LSAT, SAT, and ACT"** queued for December 7
      (Maya Chen). Five free GMAT reports within 48 hours of the Official Score, four GRE
      reports on test day, none on the LSAT (a $45 law school report per application), four
      SAT reports until nine days after a weekend test, and four ACT colleges named at
      registration, with what each later report costs and which scores it sends. Checking
      the draft against ETS's page caught a wrong claim before commit: GRE takers view their
      scores at the test center before choosing, so only the SAT's and the ACT's free
      reports go out before a score exists. EDITORIAL.md gains a sending scores block.
- [x] **"What Are the Score Ranges for the GMAT, GRE, LSAT, SAT, and ACT?"** queued for
      December 5 (James Corbett). Each exam's scale from its test maker's page, read on
      September 27: the GMAT Focus 205 to 805 with its 60 to 90 sections (and the 10th
      Edition's 200 to 800 compared only by percentile), the GRE's three scores with no
      total, the LSAT's raw score converted to 120 to 180, the SAT's sum of two 200 to 800
      sections, and the ACT's 1 to 36 Composite. It closes on what the test makers say about
      comparing across exams: ACT and College Board's concordance, which ACT calls an
      estimate, and GMAC's position that the GMAT is not equated with any other test.
      EDITORIAL.md gains a score scales block, and INC-0181 now cites the merge that fixed it.
- [x] **Every ledger record cites its commit, and the weekly harvest is level** (INC-0181).
      The harvest read incident ids only when written out in full, so the squash titles
      that name a range ("INC-0104 to INC-0110", "INC-0173 to INC-0175") left seven records
      citing nothing; and it matched candidate commits by short hash against citations
      written in full, so 57 fixed commits came back every week as possible unrecorded
      defects, 38 of them on the last run. It now reads ranges and short lists and counts a
      commit cited in full or short, and --backfill filled 77 citations from main's
      history. The five candidates left were read and cleared with reasons in
      cleared.jsonl: validation or design language in two, a claim the same change made
      stale in one, and follow-on work on INC-0079 and INC-0057 in two. The harvest now
      reports the ledger level with the repository. Still open: 24 of the earliest
      citations point at commits no longer on main whose PRs landed without a "(#N)"
      title, so nothing can repoint them automatically.
- [x] **Exam facts with no number, read by their words** (INC-0180). The GMAT's delivery
      line said appointments are available year round with no fixed testing windows, and
      the mba.com register page it cites no longer says either. The source check compares
      numbers, and 20 of the 113 exam facts have none, so it had counted them as checked
      with nothing to look for. It now reads such a fact by its words, a plural or another
      tense counting, and its summary counts those facts apart. Run over the data it
      flagged 14; all 14 were read against their pages on September 27 and now say what
      the pages say. Four had claims no page of theirs made and are re-cited: the GMAT's
      Quant calculator rule to GMAC's Data Insights guide, the SAT's uses to College
      Board's "What are SAT scores used for?", the ACT superscore's arithmetic to ACT's
      superscore FAQs, and the LSAT writing sample reaching law schools to LSAC's law
      school reports page. The queued December 1 post and the SAT format post repeated two
      of them and are corrected. support.mba.com refused every read that day (403), so
      the GMAT calculator rule cites GMAC's guide rather than mba.com's calculator policy
      article, and mba.com's exam content page answered every read with Imperva's challenge.
- [x] **"Can You Take the GMAT, GRE, LSAT, SAT, or ACT at Home?"** queued for December 3
      (David Okafor). The GMAT online (not in Mainland China, Cuba, Iran, North Korea or
      Sudan; US$300 against US$275 at a test center) and the GRE at home (24 hours a day,
      7 days a week) with each one's equipment and room rules; the LSAT's move to test
      centers from August 2026 with LSAC's four remote exceptions and its writing section
      still online; and the SAT and the ACT, given only at schools and test sites, with
      College Board's device lending and ACT's three testing modes. Every rule was read on
      the test makers' pages on September 27; EDITORIAL.md gains a block on where you can
      test.
- [x] **Five more long reading passages** (cheese, millfires, wolves, lakebloom,
      registers): a regional cheese credited to an abbey's recipe that grew famous with the
      railway; cotton mill fires blamed on careless workers, started by fibre heated in the
      faster carding engines; wolves whose return followed forest regrowing on abandoned
      farms rather than the end of a bounty; lake blooms blamed on farm fertiliser, fed by a
      sewage main; and parish register gaps blamed on the plague, left by clerks who went to
      better-paid work at the ports. They run 283 to 311 words, share no researcher or place
      with another passage (a first draft reused Oster, Tarn and Pell from existing passages
      and three names from other banks, all renamed), and pass the premise, answer tell and
      key spread checks. The banks grow by 50 GMAT, 50 GRE and 50 LSAT items: GMAT 34212,
      GRE 20588 and LSAT 14492, of which 14120 are generated. Every new item was read at
      LSAT, GMAT and GRE length, and each GRE rendering splits into its six sentences.
      Reading them caught the cheese passage's revision opening with its place name, which
      the stated-idea choices printed as "ardley cheese" (INC-0179); the corpus check now
      refuses a lowered sentence that opens with a name the passage capitalises
      mid-sentence, and over all 62 passages it flags only that one.
- [x] **"How Long Is the GMAT, GRE, LSAT, SAT, and ACT?"** queued for December 1 (Aisha
      Thompson). Each exam's testing time and sections from the checked timing facts: the
      GRE about 1 hour 58 minutes, the SAT 2 hours 14, the GMAT 2 hours 15, the ACT 2 hours
      45 with science (125 minutes without), and the LSAT about 3 hours with no published
      question counts, with a table of the average time each section allows per question,
      worked out from the test makers' figures.
- [x] **"How Long Are GMAT, GRE, LSAT, SAT, and ACT Scores Valid?"** queued for November
      29 (Elena Rodriguez). GMAT scores are valid for five years and reportable for up to
      10, GRE scores reportable for five years, LSAT scores for five testing years with
      nothing before July 2021 counting, and neither College Board nor ACT gives an expiry
      date, though both charge more to send old scores. New key facts for GMAT's 10-year
      reporting, LSAT's July 2021 cutoff and College Board's archive rule put the post's
      statements under the weekly source check; EDITORIAL.md gains a validity block.
- [x] **"When Do GMAT, GRE, LSAT, SAT, and ACT Scores Come Out?"** queued for November 27
      (Sarah Whitfield). Each test maker's rule, read on September 27, with this testing
      year's release dates for the LSAT, the SAT and the ACT from the same tables the test
      date pages use: GMAT within 5 days (up to 20), GRE 8 to 10 days, LSAT 18 days after
      each administration's last test day with an approved writing sample on file, SAT 13
      days after each fall weekend test, and ACT about 2 to 4 weeks for over 97 percent of
      scores. ACT's online testing page gives wider ranges, and the post says which page
      says which. A new ACT fact and a fuller GRE one put the post's statements under the
      weekly source check; EDITORIAL.md gains a score release block.
- [x] **The LSAT's score release, and number words in the source check** (INC-0177). The
      LSAT guide said scores come out "roughly three weeks after each administration",
      citing LSAC's dates page, which is a table of dates releasing scores 18 days after
      each administration's last test day and says nothing of three weeks; the writing
      sample's three-week processing sat on the scoring page it did not cite. It now says
      what LSAC says: scores come out on the published date with an approved writing sample
      on file and no holds, citing both pages. The check had never looked because it read
      the fact's numbers as digits only, and 34 of 109 exam facts spell one out. It now
      reads them as words too, and a number only inside a date never counts as beside the
      fact's words; that also turned up the ACT cost note's "all three", our own count,
      and the five Data Insights question types GMAC lists, now declared as a count.
- [x] **Title Case on every built heading, checked by the build** (INC-0176). The blog
      build checked the headings inside posts, and nothing read the rest: the blog
      template's "Keep reading" and "Frequently asked questions" sat on every post, and the
      trainer app, the test date pages' FAQ questions, the rankings page, the funding page
      and the diagnostic guide carried more. Each is now in Title Case; the flashcard
      round's result heading keeps to two words and moves its sentence under it, and the
      exam guides' "What It Is For and Who Accepts It" becomes "Uses and Acceptance". The
      Title Case helper moves to `page_checks.py`, learns that a subtitle after a question
      mark or a numbered prefix starts afresh and that an initial or "A&M" keeps its
      capital, and build.py and the blog build now check every h1 to h3 on every built
      page, skipping headings a script assembles and school and college names. Still to
      do: game names written two ways in body copy ("Boss round", "Boss Round").
- [x] **Title Case on every button label, checked by the build** (INC-0178). The rule names
      buttons beside headings, and 27 styled button labels broke it: "Open the trainer" on
      138 study guide pages, "Start a free round" on every blog post, the diagnostic's
      "Take the diagnostic" and "Skip this one", and a score of trainer app buttons ("Start
      drill", "Back to deck", "Study due cards", "Sign out"). Each is now in Title Case, and
      so is the blog's "Put This Into Practice" card. build.py and the blog build check
      the label of every button and link with the btn class, reading each tag's quoted
      attributes whole; a tag a script assembles no longer lets one match run on for 52,000
      characters, which on the first try passed off part of an onclick as "Sign out"'s label.
- [x] **"How Many Times Can You Take the GMAT, GRE, LSAT, SAT, and ACT?"** queued for
      November 25 (Maya Chen). Every limit comes from the test maker's own page, read on
      September 27: the GMAT's 5 in a rolling 12 months with 16 days between, the GRE's 5 in
      any 365 days with 21 between, the LSAT's 5 since July 2021 and 7 in all, and no limit
      on the SAT or the ACT, with what each counts as an attempt. The GMAT and GRE retake
      facts now say that canceled scores count, and a new LSAT fact records what does and
      does not count against LSAC's limits, so the weekly source check reads each rule the
      post states. EDITORIAL.md gains a retake block.
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
- [x] **Ten more LSAT arguments for Argument Parts and Structure**: `src/gen/g_lsat_struct.py`
      gains ten arguments written with their parts labelled (a harbour's dredging, a school's
      music lessons, a newspaper's printed edition, a second fire station, codling moth traps,
      a hospital shuttle, high street plane trees, dogs in a nature reserve, late-night buses
      and a festival's site), each asked about as five role questions and one main conclusion
      question, so the category's generated items go from 180 to 240. Every argument passes
      check_args, and all 60 new items were read before they went in. Reading them found
      that the main conclusion explanation ran a claim with a comma of its own into the
      template's next words ('where the water has warmed the most and is offered as a
      reason'), in 8 live items and 4 new ones (INC-0195): both templates now end the
      sentence after such a claim, and check_args reads every sentence an argument is
      quoted in and fails the build on the seam.

### Next session queue

- [ ] More reading passages: every reading category is still far under target, and each
      passage adds ten GMAT items and ten GRE items, plus ten LSAT items at LSAT length
- [x] Read the hand-written reading items against the same two checks (the rule is printed;
      no choice is answerable by matching words); done September 28 as INC-0192, below
- [ ] Refresh the remaining class profiles as schools post their fall 2026 classes; MIT Sloan
      first, once its page can be read. Checked September 26: the class profile pages of HBS,
      Stanford, Wharton, Booth, Kellogg, Yale, Tuck, Haas and Darden all still show the Class
      of 2027, so there is no newer class to publish yet; recheck in October. HBS, Booth,
      Yale, Tuck and Haas were read against the library and match it (Booth's page carries a
      stale Class of 2026 block beside the 2027 one, which a text summary conflates; the raw
      page confirms the library's figures)
- [ ] Bring `supabase/migrations/` in line with the live project, after the owner confirms how
      the Supabase GitHub integration deploys. The "Supabase Preview" check has failed on every
      push to main read on September 29 (pull requests show it skipped) with "Remote migration
      versions not found in local migrations directory": the project lists 43 migrations and the
      folder holds 32 files, about 26 of the remote versions have no file, and several local
      files carry a date-only version (`20260916_client_errors_sentinel.sql`) that matches
      nothing remote, two of them duplicates of timestamped files. If the integration deploys
      to production from main, fixing only the missing files would let it try to apply the
      date-only ones to the live database, so the fix has to make the folder equal the remote
      list exactly, with the SQL read from `supabase_migrations.schema_migrations`, and apply
      nothing.
- [ ] `src/smoke_load.js` stays out of CI because timing on shared runners is noisy, so run
      it by hand after any change to how the banks are split or loaded (INC-0113)
- [ ] School figures the `--schools` run could not settle from this sandbox. After INC-0159
      the run of September 27 ends at 0 figures with a number their page does not print and
      0 pages showing none of their figures, with 12 triaged (Kellogg's middle 80 percent
      ranges, drawn only as box plots, and WashU Olin's class profile, drawn only as images)
      and 14 sources unreadable: Columbia, Michigan Ross and Bloomberg, which refuse a script
      and answer the browser with a bot challenge (Baylor's, which refused only the script,
      and Fordham's, which loop a script through redirects, are read in the browser);
      certificate failures at Penn State Smeal and UC Irvine Merage (not to be bypassed); US
      News, which answers the browser with plain text; Wharton's career report; and Olin's
      Class of 2024 report, an image-only PDF read by eye on September 27. The six pages once written off as built
      by JavaScript were three that had changed (Kelley, Maryland on Poets&Quants, Auburn),
      two the check misread (UMass Amherst's PDF, Booth's workbook) and one drawn as images
      (WashU Olin's). Cincinnati keeps its labelled 2025-26 tuition until the school page can
      show a range: from 2026-27 UC bills the Lindner MBA per credit hour over 35 to 48 credits
- [x] Emory Goizueta's acceptance rate (32 percent, from Poets&Quants) disagreed with its own
      source label: 450 admitted of 1,581 applications is 28.5 percent. Read on September
      27 (INC-0168): the article prints 32% in its table and its text and credits the data
      to Emory; every earlier year in its table matches its counts and the new class's
      yield matches the 450 admits, so either the rate or the 1,581 is misprinted and the
      article does not say which. The page keeps the printed 32%, its source line no longer
      implies the counts produce it, and its note gives the 28.5 percent the counts work out
      to. Emory's own class profile prints no admissions figures.
- [x] Six GMAT facts cite pages this sandbox could not read: four on www.mba.com served a
      bot challenge and two on support.mba.com answered 403. Since INC-0156 and INC-0159 the
      check reads them in the browser, and the run of September 27 read all of them except
      GMAC's policies PDF, which Imperva challenged on some reads and served on others
      (INC-0175); its two facts were read against a direct fetch of the PDF the same day

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
