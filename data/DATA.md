# School Library: Schema and Source Policy

One file per school in `data/schools/<slug>.json`. The build
(`src/build_rankings.py`) loads every file in the directory, validates it with
`src/validate_schools.py`, computes the SFN Score, and generates `/schools/`
plus one page per school. Editing a school means editing its file; adding a
school means adding a file. Never edit generated output.

## File Shape

```
{
 "slug": "stanford-gsb",            unique, kebab-case, becomes the URL
 "name": "Stanford Graduate School of Business",   stands alone: never just "School of Business"
 "university": "Stanford University",
 "city": "Stanford", "state": "CA",
 "region": "West",                  Northeast | Midwest | South | West
 "type": "Private",                 Private | Public
 "website": "https://...",          official program site
 "discontinued": true,              optional; excluded from rankings when true
 "notes": "...",                    optional, plain text; cite discontinuation sources here
 "official_hosts": [                optional; hosts outside the school's domain where the
   {"prefix": "https://...",         school itself publishes (its storage bucket, an alias
    "evidence": "...",               domain). Needs evidence and a checked date; a figure
    "checked": "2026-09-26"}         under a prefix is labeled the school's own, not
 ],                                  secondary. Never a publisher (validator refuses one).
 "ranks": {
   "usnews": {"rank": 1, "edition": "2026", "url": "https://..."},
   "ft": ..., "bloomberg": ..., "qs": ..., "pq": ...
 },
 "profile": {
   "class_year": "Class of 2027",
   "gmat_focus":  {"v": 689, "stat": "average", "src": "...", "year": 2025, "url": "https://..."},
   "gmat_classic": ..., "gre_quant": ..., "gre_verbal": ...,
   "gpa": ..., "accept_rate_pct": ..., "class_size": ..., "work_exp_years": ...,
   "women_pct": ..., "intl_pct": ..., "tuition_usd": ..., "program_cost_usd": ...,
   "salary_median_usd": ..., "employment_rate_pct": ...
 }
}
```

`name` is printed on its own in a page's title, heading and every answer, so it says which
school it is: "UC Riverside School of Business", not the "School of Business" that the
school's site can print under its university's banner. The validator refuses a name made
only of words like school, college, business and management (INC-0153).

A figure's `stat` describes it as its source states it ("average", "2026-27 rate, tuition
only"), and is printed beside it and checked against its page. A figure's `note` is our
commentary on how it was read, and is neither printed nor checked, so it sits beside a
`stat` and never replaces one; the validator refuses a figure with a note and no stat
(INC-0143).

`class_year` names the class the profile describes in words that say what the year is:
"Class of 2027" for a graduating class, "Fall 2025 entering class" for the class that
entered then, "2019-20" for a profile dated by academic year, "Three-year average of the
Classes of 2026, 2027 and 2028" for a profile that averages several classes and shows no
single one (read as an average over all of them, never as its first class), or "Typical
class profile (no class year stated)" when the page names none. A bare year is refused, because it
cannot say which of those it means; six records used one for the year a page was read or
the cycle it serves and were printed as a Class of that year (INC-0147). A figure takes
the class its own `stat` names, else the one its `src` names, else the record's; a figure
whose `stat` says its page labels no class year takes none.

A figure is read on its page, never from a search result's snippet of the page: the
validator refuses a published figure whose `stat`, `note` or `src` says snippet, because
Rice's GMAT was taken from one and cited to an article that never prints it (INC-0151).

`tuition_usd` is tuition for one year. `program_cost_usd` is the figure a school
publishes for the whole program, for the schools that price the program and never a
year: a total, a program fee, or an estimate of the whole. It is never divided into a
year, never added to the SFN Score or the tuition column and filter, and never filled
by multiplying a per-credit rate by a credit count, because students do not all take
the same number of credits. Where a school prices by residency, `v` is the figure for
an out-of-state student and the resident figure goes in `stat`. Where the page prints
tuition apart from fees, `v` is the tuition; otherwise it is the page's combined
figure, and `stat` says which. A page that names no academic year keeps the year it
was read in `year` and says so in `stat`.

`employment_rate_pct` is measured at some point after graduation, and its `stat` must
say when, in the words the school uses ("within 3 months", "90 days", "six months",
"within a year", "reported up to October 31"). The build reads the first timing the note
names for the figure's label. Only a three month figure, or one whose timing the note
leaves unverified, is scored or sorted with the others; a figure measured at another
point is shown with its timing and does neither (INC-0142).

## Hard Rules (validator enforces)

1. Every published value carries `src`, `year`, and `url`. A figure we cannot
   verify is `{"v": null}` or omitted, never a guess.
2. GMAT Focus (205 to 805) and Classic (200 to 800) are separate fields and
   are never converted or mixed. `stat` records average vs median, and says which
   edition the source gives the figure in the source's own words: the edition's
   name ("GMAT Focus", "10th Edition", "Legacy", "Traditional exam (older
   version)"), its scale, or the other edition named beside it ("listed as GMAT
   beside a separate GMAT Focus figure"). A source that names no edition does not
   settle it, and neither does the number: an average or median can end in any
   digit, both scales reach 800, and scores of either edition stay valid for five
   years (GMAC), so any class that enrolled from 2024 on can hold both. The one
   proof outside the source is a class that took the test before GMAT Focus testing
   began on November 7, 2023 (GMAC, August 29, 2023), recorded in
   `edition_proof` with its reason, the https pages that show it and the date
   checked. Otherwise the figure is blank, with a note quoting what the source
   prints (INC-0157). The validator enforces all of this.
3. Banned sources (build fails): GMAT Club, Quora, Wikipedia, GyanDhan,
   Pagalguy, Reddit, any forum.
4. Weak sources (build warns, replacement queued): Clear Admit, Stacy
   Blackman, F1GMAT, Leland, anything labeled "search snippet". Prefer the
   school's own class profile and employment report pages.
5. No em or en dashes anywhere.
6. Values must sit in plausible ranges (see validate_schools.py); an
   out-of-range value is treated as a data entry error.

## Source Preference Order

1. The school's official class profile / admissions statistics page.
2. The school's official employment report (PDF or page), for salary and
   employment rate.
3. A tracked publisher's data table (US News, FT, Bloomberg, QS, Poets and
   Quants) when the school itself does not publish the figure.

A figure counts as the school's own when its URL shares the registrable domain of the
program website (bursar.rice.edu is Rice; a university news office is the university) or
sits under one of the school's `official_hosts`. Anything else is marked secondary on the
page with an asterisk and a footnote.
4. Nothing else.

## Ranking Methodology

Weights and formulas live in `src/build_rankings.py` and are printed verbatim
on the public methodology section. If the weights change, the page text
changes with them in the same commit.

# Exam Content Sources

`data/exams.json` holds one record per exam for the public guides at
`/exams/<slug>/`, with `src`, `year` and `url` on every fact. The same rule
covers anything the trainers encode about an exam's structure: a section
length, a domain label, or a question range is either sourced or absent.

A citation proves a source is named, not that it says the figure (INC-0130), and a
publisher changes its fees on its own schedule (INC-0132). `python3 src/check_sources.py`
reads every page and PDF the file cites and reports each number in a fact, or in its
`note`, that the source does not print. It reads a page as a person sees it: text inside
an HTML comment is left out, because a school that retires a figure often comments it out
rather than deleting it, and Arizona State's 43 percent women was confirmed from such a
row (INC-0152). An image's alt text is read with the page, because it is the text the page
gives in the image's place: Berkeley Haas and Pitt Katz draw their figures as images and
write the figures into the alt text (INC-0154). A bot challenge is never read as the page it
stands in for: a short read in a challenge's words (Imperva's security check on mba.com,
Cloudflare's Just a moment) is not cached, and the source is reported unreadable rather than
missing the figures (INC-0156). A page that refuses the plain read with 401, 403 or 429 is
read in the browser, under the same user agent, before it is called unreadable: Baylor's
pages refuse a script and render for a browser, while Columbia's, Michigan Ross's and
Bloomberg's answer the browser with a challenge as well, which is reported as one (INC-0159).
A page that sends a script round a redirect loop, as Fordham's login gateway does, is read in
the browser the same way.
A browser read that gets a challenge is tried once more a few seconds later, because Imperva
challenges mba.com on some reads and not others. An exam figure is published from its value
or text only: the note of a figure with no value is never printed, and validate_exams refuses
a dollar amount there, since the GMAT's cost tile once showed prices from such a note that no
check read (INC-0160). A figure a page shows only after a choice, as mba.com shows the GMAT's
fees once a country is chosen, is read from the address the page loads it from, named in
`also_urls` and held by validate_exams to the test maker's host.
It runs weekly in `.github/workflows/playbook.yml`
and opens an issue when something no longer matches. A fact whose number is arithmetic on
its source says so with a `derived` entry giving the working, such as
`"derived": {"63": "21 + 42, the private and public colleges the page lists"}`, and the
check then looks for the inputs instead; a number read off the page rather than printed as
one, counted from a list or split into separate characters, begins its entry with
`count:`. Pages that build their text with JavaScript need `--render`, which reads them in
Chromium through `src/render_page.js` the way a person would: it scrolls to the bottom so
charts that draw only when seen get drawn, and reads every visible frame, since some class
profiles are embedded charts in frames of their own (Stanford's and Wharton's are
Infogram charts). It leaves PDFs to the ordinary read and skips hidden frames, whose
text is raw source, and the browser's read replaces the page as served only when it shows
at least as many of the cited figures (INC-0146). `--schools` runs the same check over the
school library (INC-0133): it sets aside College Scorecard figures, which come from a
dataset rather than a page, leaves a figure's `note` out because there it is our
commentary, and reports a page that shows none of its figures, with what the page prints
beside each figure's label (INC-0158). Other numbers there mean the page has probably moved
on to a newer class: Kelley's page showed the Class of 2028 while the library published
the Class of 2027, and was written off as a page built by JavaScript, because a page whose
every figure changed looks, to a check for numbers, like a page that never loaded. Such a
page fails the run until its figures are fixed or triaged. The check reads what a person
sees in places a plain text read misses: a counter that counts up from 0 is read at the
figure in its `data-target` attribute (Auburn), a figure a PDF's text layer glues to its
label ("GPA3.45") is split from it (UMass Amherst), and an Excel workbook is read as its
cells display, 87.8% rather than 0.878 (Chicago Booth), which needs `pip install xlrd`.
For a school figure it also asks where the number sits (INC-0150): a number found only
away from a word saying what it counts is reported as not found, and one found beside its
label only near another program's name (MBAxMS, executive, part-time, evening) is listed as
worth reading, since comparison tables and footnotes do that to figures that are right.
Columbia's MBA class carried five years of work experience that the article gives for its
MBAxMS cohort, and a check that only looked for the number could not tell. An exam fact is
held to the same question (INC-0174): each of its numbers must sit within 160 characters of
one of the fact's own words, or, for a figure with no text such as a score validity, of a
word its field is about (valid, reportable, expire), or be a cell in a run of numbers, which
is how a table prints it. GMAC's retake article confirmed the GMAT's five-year validity with
"up to 5 times", and its score release article confirmed "3 to 5 days" with the 3 of "0 out
of 3 found this helpful". Markup is read with an HTML parser rather than patterns, because a
quoted attribute can hold markup: ETS keeps a copy of each text block in one, and a pattern
that ended the tag at its first > read an element id's 5 as GRE's score validity (INC-0173).
A fact's numbers are read in words as well as digits, as a page's always were, so "roughly
three weeks" is looked for like "3 weeks", and a number that is only part of a date such as
3/3/2027 counts as found but never as beside the fact's words: the LSAT guide said scores
come out roughly three weeks after each administration, which neither LSAC page says, and
the check had never looked (INC-0177). A number a fact counts off a page's list, such as the
five Data Insights question types GMAC lists without numbering them, is declared with a
`count:` entry.
Imperva's script challenge, a short page whose only content is a script from
`/_Incapsula_Resource`, has no words to recognise it by; a plain read that gets it is tried
once more and then reported as a challenge, and no read too short to be evidence is cached
(INC-0175).

A figure worked from two pages cites the second in `also_urls`, a list of https urls, and
the check reads it with the first: Cincinnati's tuition adds the out-of-state surcharge
from UC's surcharge page to the fee on its fee page. A school figure that is right but that
the check cannot read, such as a range Kellogg draws only as a box plot, goes in
`data/source_triage.json` once a person has read it on its page: its key
(`slug.profile.field`), its value, the numbers the check misses, why, and the date it was
read. The check lists those apart and fails only on a finding nobody has judged, so the
weekly issue shows what is new; 13 real errors once sat unworked among 30 findings, 14 of
them right figures the check could not then read (INC-0154). validate_schools refuses an entry whose
figure has gone, has changed value, or no longer carries the numbers it lists, so a
judgement never outlives the figure it was about. Teach the check to read a figure before
triaging it.

A page can be quoted exactly and still be out of date: LSAC's LSAT FAQ went on describing
"the 2025-2026 testing year" after LSAC moved almost every test taker into test centers
(INC-0136). So for the exam guides the check also reports every fact cited to a page that
says it covers a testing, academic or school year that has ended. Read the fact against a
current page; if it still holds, record that on the fact, for example
`"period_checked": {"periods": ["2025-2026"], "on": "2026-09-27", "why": "the specifications
page, current for 2026-2027, still gives the same sections"}`, and the report stays quiet
until the page names another ended year.

The SAT and PSAT/NMSQT calculators' percentiles in `data/sat_percentiles.json` and
`data/psat_percentiles.json` are College Board's, parsed from its research pages by
`python3 src/sat_percentiles.py --write`, which also quotes each page's definitions word for
word, the fall 2026 Understanding Scores guides' rule that a total is the sum of the two
section scores, the NMSC Selection Index rule from College Board's What Do My Scores Mean?
page, and the PSAT/NMSQT guide's grade-level benchmarks, read off its table. Nothing in
either file is typed. The weekly job runs `--check`, which re-reads both pages and reports
any cell, row or definition that changed. The LSAT percentile calculator's table in
`data/lsat_percentiles.json` is LSAC's, parsed the same way by `python3 src/lsat_percentiles.py
--write` from LSAC's Data Library, with LSAC's own sentences on the scale, the score report
and score bands quoted; its `--check` runs weekly too, since LSAC updates percentiles every
year by the end of July.

The test date pages under `/exams/<exam>/test-dates/` come from `data/test_dates.json`:
College Board's SAT Weekend table and its fall score release table, ACT's national test
dates table and LSAC's two LSAT tables, parsed by `python3 src/test_dates.py --write` row by
row under the header each page prints. A row whose dates do not run in order is refused
rather than guessed, a date printed without a year takes the year that puts a deadline
before its test and a score release after it, and a sentence a page is quoted with is kept
only if the page prints it word for word. Nothing in the file is typed. The weekly job runs
`--check`, which re-reads all four tables and reports any date, row or table that moved.
The pages lead with where registration stands on the reader's own day, never the next test
date alone, and each date downloads as a calendar file whose events carry the table's own
dates, which `src/smoke_dates.js` checks against the file.

## SAT, as encoded in `src/engine.js`

| What | Where it comes from |
| --- | --- |
| Section structure and timing: Reading and Writing two 32-minute modules of 27 questions, Math two 35-minute modules of 22 | College Board, SAT test structure, https://satsuite.collegeboard.org/sat/whats-on-the-test/structure |
| Total score 400 to 1600, sections 200 to 800 | Same page, and Table 4 of the specifications overview below |
| Section-adaptive delivery: performance on module 1 determines the form of module 2 | Same page |
| The eight content domains, and the skill and knowledge points under each | College Board, What Are Content Domains?, https://satsuite.collegeboard.org/practice/content-domains |
| Question distribution per domain (Craft and Structure 13 to 15, Information and Ideas 12 to 14, Standard English Conventions 11 to 15, Expression of Ideas 8 to 12; Algebra 13 to 15, Advanced Math 13 to 15, Problem-Solving and Data Analysis 5 to 7, Geometry and Trigonometry 5 to 7) | Tables 2 and 3, The Digital SAT Suite of Assessments Specifications Overview, https://satsuite.collegeboard.org/media/pdf/digital-sat-test-spec-overview.pdf |
| Reading and Writing module order: Craft and Structure, then Information and Ideas, then Standard English Conventions, then Expression of Ideas, each group easiest to hardest | Same document, Reading and Writing content domains section |
| Math questions arranged easiest to hardest across each module | Same document, Math content domains section |

Two things are deliberately ours and are labeled as ours wherever a student
can see them:

1. **The routing threshold.** College Board does not publish the rule it uses
   to decide which second module a student receives. `SAT_ROUTE_CUT` in
   `src/engine.js` is 60 percent, and the routing screen says so in those
   words rather than implying an official cutoff.
2. **The scale anchoring.** The equating tables that turn raw performance
   into a 400 to 1600 score are not public. Since the owner's decision of
   September 16, 2026 the app does report an estimated range on the SAT's own
   scale, but the centre and slope in `EXAMS.sat.scale` are our calibration,
   not College Board's. The app says so, never calls the output a predicted
   score, holds it back below the evidence floor, and points students to an
   official Bluebook practice test to calibrate. The method is published at
   `/scoring/`.

Per-question pace (`allot`) is arithmetic on the sourced module lengths, not a
published figure: 32 minutes over 27 questions is 71 seconds, 35 over 22 is 95.

## LSAT, as encoded in `src/engine.js`

| What | Where it comes from |
| --- | --- |
| Four 35-minute multiple-choice sections: one Reading Comprehension, two Logical Reasoning, one unscored variable section that can be either type and can appear anywhere | LSAC, Specifications of the LSAT and LSAT Argumentative Writing, https://www.lsac.org/lsat/register-lsat/accommodations/specifications-lsat-and-lsat-argumentative-writing |
| A 10-minute intermission between the second and third sections | Same page |
| Scores 120 to 180; raw score is the number answered correctly; every question weighted the same; no deduction for a wrong answer | LSAC, LSAT Scoring, https://www.lsac.org/lsat/lsat-scoring |
| Reading Comprehension section shape: four sets, each a selection followed by five to eight questions, with three or four single passages and one or no comparative pair | LSAC, Reading Comprehension, https://www.lsac.org/lsat/prepare/types-lsat-questions/reading-comprehension |
| The ten skills Logical Reasoning measures, grouped into the seven tracked skills | LSAC, Logical Reasoning, https://www.lsac.org/lsat/taking-lsat/test-format/logical-reasoning |
| The ten passage characteristics Reading Comprehension questions ask about, grouped into the five tracked skills | LSAC, Reading Comprehension, as above |
| Five answer choices per question | LSAC, Logical Reasoning Sample Questions, https://www.lsac.org/lsat/taking-lsat/test-format/logical-reasoning/logical-reasoning-sample-questions |
| LSAT Argumentative Writing is unscored, administered separately, 50 minutes total (15 prewriting, 35 writing) | LSAC, Types of LSAT Questions, https://www.lsac.org/lsat/prepare/types-lsat-questions |

Two things are ours and are labeled as ours:

1. **The Logical Reasoning section length.** LSAC publishes 35 minutes per
   section but no question count for Logical Reasoning, anywhere. The
   25-question practice section is our own length, chosen to fit the published
   35 minutes. The exam guide and the trainer footer say so rather than
   presenting 25 as an LSAT specification. Reading Comprehension's 26 is also
   ours, but it sits inside the 20 to 32 that LSAC's published "four sets of
   five to eight questions" implies.
2. **The scale anchoring**, exactly as for the SAT above.

One thing is deliberately absent. **The LSAT reports no section scores.** LSAC
reports a single number and publishes no subscores, so `EXAMS.lsat.scale`
carries no `sectionMin` or `sectionMax` and `scoreEstimate` returns
`score: null` for every section. `test.js` fails the build if that exam ever
starts emitting a per-section number. We train one Logical Reasoning section;
the real exam delivers two.

## ACT, as encoded in `src/engine.js`

| What | Where it comes from |
| --- | --- |
| Section lengths and timing: English 50 questions in 35 minutes, Mathematics 45 in 50, Reading 36 in 40, optional Science 40 in 40, optional Writing one essay in 40 | ACT, Preparing for the ACT Test 2026-2027, https://www.act.org/content/dam/act/unsecured/documents/Preparing-for-the-ACT.pdf |
| Scored counts, which are lower than the administered counts because every section carries embedded unscored field-test questions: English 40, Mathematics 41, Reading 27, Science 34 | Same booklet |
| 171 multiple-choice questions total and 2 hours 45 minutes of timed testing | ACT, Test Day, https://www.act.org/content/act/en/products-and-services/the-act/test-day.html |
| Four answer choices in every section, Mathematics included | Same booklet, practice test forms and the Mathematics tips section |
| Sections and Composite scored 1 to 36; Composite is the average of English, Mathematics and Reading, rounded; Science removed from the Composite in April 2025 for national online testing and September 2025 for all modes; Writing scored 2 to 12 across four domains | ACT, Understanding Your Scores, https://www.act.org/content/act/en/products-and-services/the-act/scores/understanding-your-scores.html |
| The fifteen reporting categories and the percentage of each section devoted to each | Same booklet, Content of the ACT sections |
| Fees: $70.00 base, $5.00 science add-on, $25.00 writing add-on, $100.00 for all three | ACT, Fees, https://www.act.org/content/act/en/products-and-services/the-act/registration/fees.html |

Two things are ours and are labeled as ours:

1. **The scale anchoring**, as above. The centre and slope in
   `EXAMS.act.scale` are our calibration; ACT publishes no equating table.
2. **Nothing else.** Every structural figure above is ACT's own, which is why
   the earlier Applerouth, Kaplan and BestColleges rows in `data/exams.json`
   were replaced: they are coaching-site sources, which this project bans, and
   the fee figure had drifted (they carried $68 and a $4 science add-on
   against ACT's published $70 and $5).

`inComposite: false` on the ACT Science section is how the engine keeps a
section that is scored and reported out of the headline average. It is rated,
it appears in the section report, and it is not averaged into the Composite,
which is what ACT does.
