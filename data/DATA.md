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
