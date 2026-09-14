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
 "name": "Stanford Graduate School of Business",
 "university": "Stanford University",
 "city": "Stanford", "state": "CA",
 "region": "West",                  Northeast | Midwest | South | West
 "type": "Private",                 Private | Public
 "website": "https://...",          official program site
 "discontinued": true,              optional; excluded from rankings when true
 "notes": "...",                    optional, plain text; cite discontinuation sources here
 "ranks": {
   "usnews": {"rank": 1, "edition": "2026", "url": "https://..."},
   "ft": ..., "bloomberg": ..., "qs": ..., "pq": ...
 },
 "profile": {
   "class_year": "Class of 2027",
   "gmat_focus":  {"v": 689, "stat": "average", "src": "...", "year": 2025, "url": "https://..."},
   "gmat_classic": ..., "gre_quant": ..., "gre_verbal": ...,
   "gpa": ..., "accept_rate_pct": ..., "class_size": ..., "work_exp_years": ...,
   "women_pct": ..., "intl_pct": ..., "tuition_usd": ...,
   "salary_median_usd": ..., "employment_rate_pct": ...
 }
}
```

## Hard Rules (validator enforces)

1. Every published value carries `src`, `year`, and `url`. A figure we cannot
   verify is `{"v": null}` or omitted, never a guess.
2. GMAT Focus (205 to 805) and Classic (200 to 800) are separate fields and
   are never converted or mixed. `stat` records average vs median.
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
2. **The absence of a scaled score.** The equating tables that turn raw
   performance into a 400 to 1600 score are not public. The app reports
   accuracy, per-domain results against the official ranges, and which module
   a student routed into. It never reports a score, and it points students to
   an official Bluebook practice test to calibrate.

Per-question pace (`allot`) is arithmetic on the sourced module lengths, not a
published figure: 32 minutes over 27 questions is 71 seconds, 35 over 22 is 95.
