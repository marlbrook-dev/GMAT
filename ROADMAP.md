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
