# The Study Room: editorial brief

Strategy source of truth: `design/guidelines/seo-content.md`. This file adds the house rules and the verified fact sheet writers must use. Generator: `src/build_blog.py` (validates on every build and fails loudly).

## Voice
Institutional, plain, even-handed. Confident but never salesy. Short sentences. No hype words (unlock, supercharge, game-changer). Never trash competitors or other tests. American English.

## House style (build fails on violation)
- No em dashes and no en dashes anywhere. Use commas, colons, periods, or the word "to" in ranges.
- GMAT Focus Edition total scores run 205 to 805 (ending in 5); sections score 60 to 90. Never present a Classic (200 to 800) number as a Focus number or vice versa. Always label which edition a number belongs to. Compare editions by percentile, not raw score.
- Titles 60 characters or fewer, keyword in the first half. Meta description 155 characters or fewer, keyword included.
- One H1 (the generator provides it from the title). Body uses h2/h3 only, question-phrased where natural. Answer the title's question in the first 80 words.
- At least one data table per post. Internal links to at least 2 sibling posts. FAQ block of 3 to 5 Q&As.
- Categories: Exam Guides, Study Science, Success Stories, Company News.

## Data rules (non-negotiable)
- Never state a school statistic, score median, percentile, or class-profile number from memory. Use ONLY the verified fact sheet below, with the source and year in parentheses right after the number.
- Approved sources: official school websites and class profiles, mba.com / GMAC, Poets & Quants, Financial Times, US News, Bloomberg Businessweek, Forbes, BusinessBecause, QS. Never cite or link GMAT Club, Quora, Wikipedia, GyanDhan, Pagalguy, or forums.
- Never invent statistics about Start From Nowhere: no user counts, no score-gain claims, no testimonials. The product facts below are the only product claims allowed.
- Success stories are reader-submitted only. Never fabricate one.
- If a fact is not on the sheet, write around it or state that the school publishes the figure in its class profile.

## Verified fact sheet (checked August 17, 2026)

Format and scale (mba.com, GMAC, 2026):
- GMAT (Focus Edition) total 205 to 805 in 10-point steps; three sections, Quantitative Reasoning, Verbal Reasoning, Data Insights, each scored 60 to 90 and equally weighted.
- 64 questions: 21 Quant, 23 Verbal, 20 Data Insights. 45 minutes per section, 2 hours 15 minutes total, one optional 10-minute break. Test takers pick section order and can bookmark and change up to 3 answers per section.
- Versus the Classic exam: the essay (AWA), Sentence Correction, and geometry are gone; Data Insights (which absorbs Integrated Reasoning content and Data Sufficiency) now counts in the total score.

Concordance (GMAC official score concordance tables): Classic 700 = Focus 655, both 90.5th percentile. Classic 710 is approximately Focus 665; Classic 740 is approximately Focus 695. Compare percentiles, never raw scores.

Class of 2027 profiles (entered fall 2025):
- Stanford GSB: average GMAT Classic 738; average GMAT Focus 689, Focus range 615 to 785 (Stanford GSB Class of 2027 profile, 2025).
- MIT Sloan: median GMAT Classic 720, middle 80% 710 to 760; median GMAT Focus 675, middle 80% 645 to 735 (MIT Sloan Class of 2027 profile, 2025).
- Harvard Business School: median GMAT Focus 685; median GMAT Classic 730; median GRE 164 Quant and 164 Verbal; 44% of the class submitted a GRE, 34% a GMAT Focus, 28% a Classic GMAT, some submitted more than one (HBS Class of 2027 profile, 2025).
- Wharton: average GMAT Classic 735, middle 80% 680 to 770; average GMAT Focus 676, range approximately 620 to 725 (Wharton Class of 2027 profile; Poets & Quants, 2025).
Note in-text which schools report averages (Stanford, Wharton) versus medians (MIT, HBS).

Class of 2027 profiles, additions verified against each school's own class profile page on August 20, 2026 (full citations with URLs live in data/schools/<slug>.json; keep any figure quoted in a post consistent with that file):
- Yale SOM: median GMAT Focus 675 (80% range 638 to 715); median GMAT Classic 740 (Yale SOM class profile, 2025).
- Berkeley Haas: median GMAT Focus 675 (middle 80% 637 to 725); median GMAT Classic 730 (Haas class profile, 2025).
- NYU Stern: average GMAT Focus 682; average GMAT Classic 737 (NYU Stern class profile, 2025).
- Dartmouth Tuck: average GMAT Focus 671; average GMAT Classic 727 (Tuck class profile, 2025).
- Duke Fuqua: median GMAT Focus 665; median GMAT Classic 720 (Duke Class of 2027 profile via BusinessBecause, 2025).
- Texas McCombs: median GMAT Focus 655 (middle 80% 615 to 695) (McCombs class profile, 2025).
- Emory Goizueta: average GMAT Focus 648; average GMAT Classic 723 (Goizueta class profile, 2025).
- Georgetown McDonough: average GMAT Focus 625; average GMAT Classic 700 (McDonough class profile, 2025).
Note in-text which figures are averages (Stanford, Wharton, Stern, Tuck, Goizueta, McDonough) versus medians (MIT, HBS, Yale, Haas, Fuqua, McCombs).

Product facts (the only permitted product claims, updated September 14, 2026):
- Start From Nowhere runs five adaptive trainers on one engine. GMAT Focus at /app/: 34012 original practice items across Quant, Verbal, and Data Insights; 134 flashcards; seven practice games plus full mock exams. Digital SAT at /sat/app/: 20256 original items across the eight official content domains, 112 flashcards, and mock sections that run as two modules with the second routed by performance on the first. GRE at /gre/app/: 20388 original items across Verbal Reasoning and Quantitative Reasoning, 56 flashcards, section-adaptive mock sections, and an Analytical Writing task that reports measurable facts about a draft rather than inventing a score. ACT at /act/app/: 39864 original items across English, Mathematics, Reading and Science, 126 flashcards, with Science built from study data rather than recall. LSAT at /lsat/app/: 14292 original items across Logical Reasoning and Reading Comprehension, 102 flashcards. 372 are hand written and cover all twelve LSAC categories; the 13920 generated ones reach seven Logical Reasoning categories and three Reading Comprehension ones, the reading ones thinly, so a post should not imply even depth across the section.
- Every trainer keeps a rating per skill keyed to that exam's official score-report labels, return misses on a spaced schedule, and tracks timing per question. First round free, no account needed.
- Every trainer reports an estimated range on that exam's own scale (GMAT Focus 205 to 805, SAT 400 to 1600, GRE 260 to 340 as the sum of the two 130 to 170 measures, which ETS reports separately, LSAT 120 to 180, ACT 1 to 36) once a student has answered enough questions, alongside accuracy, per-domain results, and which SAT module they routed into. Write it as an estimated range from practice, never as a predicted or guaranteed score, and never as a single number. The scale anchoring is our own calibration, not the test maker's, and the method is published at /scoring/.
- The site also publishes an MBA rankings library covering 91 US full-time programs at /schools/, with a source and year on every figure. There is no undergraduate rankings library yet; do not imply one.

Digital SAT format and content (College Board, verified September 14, 2026):
- Total score 400 to 1600 in 10-point intervals; Reading and Writing and Math each scored 200 to 800 (College Board, SAT test structure, 2025).
- Reading and Writing: two 32-minute modules of 27 questions each, 54 questions in 64 minutes. Math: two 35-minute modules of 22 questions each, 44 questions in 70 minutes. 98 questions, 2 hours 14 minutes of testing, with a 10-minute break between sections (College Board, 2025).
- Section-adaptive, not question-adaptive: performance on the first module of a section determines whether the second module is the harder or the easier form. College Board does not publish the routing threshold, so never state one as official (College Board, 2025).
- Reading and Writing passages run 25 to 150 words, each followed by one multiple-choice question with four answer choices, drawn from literature, history and social studies, the humanities, and science (College Board, 2025).
- The four Reading and Writing content domains and their operational question ranges: Craft and Structure 13 to 15, Information and Ideas 12 to 14, Standard English Conventions 11 to 15, Expression of Ideas 8 to 12. Within a module the domains appear in that order, Craft and Structure first, and questions testing similar skills are grouped and run easiest to hardest (Digital SAT Suite Specifications Overview, Table 2).
- The four Math content domains and their ranges: Algebra 13 to 15, Advanced Math 13 to 15, Problem-Solving and Data Analysis 5 to 7, Geometry and Trigonometry 5 to 7. Math questions run easiest to hardest across each module (same document, Table 3).
- The Desmos graphing calculator is built into Bluebook and allowed on the entire Math section, alongside annotation, answer elimination, and question flagging (College Board, calculator policy, 2025).
- Fully digital in the US since March 2024, taken in the Bluebook app (College Board Newsroom, 2024). SAT registration fee $68, with additional fees listed through December 2026; students testing in another country are sent to a separate international fee schedule (College Board, 2026). Most scores from weekend tests are released 2 to 4 weeks after test day (College Board, 2026).
- Class of 2025 results (College Board, 2025 SAT Suite Annual Report, Total Group; each student counted once at their most recent score): 2,004,965 test takers; mean total 1029 (SD 235), Reading and Writing 521 (SD 121), Math 508 (SD 126). Total score bands: 1400 to 1600, 149,767; 1200 to 1390, 357,574; 1000 to 1190, 554,819; 800 to 990, 609,159; 600 to 790, 281,174; 400 to 590, 52,472. So 7.5 percent scored 1400 or higher and 25.3 percent 1200 or higher (our arithmetic on the counts). Score reports show an All Tester Percentile, the percent of the past three cohorts of 12th-grade SAT takers worldwide at or below a score (College Board, Understanding Scores, fall 2026).
- Students can take the SAT as many times as they want; College Board recommends at least twice, in the spring of junior year and the fall of senior year (College Board, 2026). Approved SAT sources: College Board and its SAT Suite site, and the publishers already approved above. Everything in this block is mirrored with URLs in data/exams.json and data/DATA.md; keep any figure in a post consistent with those files.

LSAT percentiles (LSAC, verified September 26, 2026; mirrored with its URL in data/exams.json):
- LSAC's percentile rank is the percentage of test scores lower than a given score, over the 2023-2024, 2024-2025 and 2025-2026 testing years (LSAC, LSAT Percentiles). It counts test scores, not people.
- 180 is 99.85, 175 is 98.72, 173 is 97.59, 170 is 94.48, 168 is 91.36, 167 is 89.53, 165 is 85.17, 163 is 80.05, 160 is 71.06, 158 is 64.48, 155 is 54.03, 154 is 50.43, 153 is 46.93, 152 is 43.37, 150 is 36.56, 145 is 21.48.

GRE percentiles (ETS, verified September 26, 2026; mirrored with its URL in data/exams.json):
- ETS percentile ranks give the percentage of test takers who scored lower than a score, from everyone who tested between July 1, 2022, and June 30, 2025 (ETS, GRE General Test Interpretive Data, Tables 1A to 1C).
- Verbal Reasoning: 170 is 99, 168 is 98, 165 is 95, 164 is 93, 163 is 90, 160 is 82, 158 is 76, 155 is 64, 153 is 54, 150 is 39, 145 is 21. Quantitative Reasoning: 170 is 89, 168 is 80, 165 is 67, 164 is 63, 163 is 60, 160 is 50, 158 is 45, 155 is 37, 153 is 31, 150 is 23, 145 is 12. Analytical Writing: 6.0 is 99, 5.0 is 93, 4.5 is 85, 4.0 is 63, 3.5 is 40, 3.0 is 16.
- Means: Verbal 151.39 (standard deviation 8.43, 788,021 test takers), Quantitative 157.62 (9.90, 790,864), Analytical Writing 3.46 (0.85, 785,720).

ACT format and scoring (ACT, verified September 26, 2026; every figure is mirrored with its URL in data/exams.json):
- English 50 questions in 35 minutes, math 45 in 50, reading 36 in 40: 131 questions in 125 minutes. Optional science is 40 questions in 40 minutes; with it the timed multiple choice runs 171 questions in 2 hours 45 minutes. The optional writing essay takes 40 minutes after a 5-minute break (ACT, 2026).
- Each section is scored 1 to 36. The Composite is the average of English, math and reading, rounded to the nearest whole number: fractions less than one-half round down, one-half or more round up. Science left the Composite for national online testing in April 2025 and for all ACT tests in September 2025; it still feeds a STEM score, the average of math and science, and an ELA score averages English, reading and writing when writing is taken. Writing is scored 2 to 12 (ACT, 2026).
- The superscore averages your best English, math and reading scores across attempts and is rounded the same way. It is calculated automatically once you have tested more than once since September 2016, it leaves out science and writing, and ACT advises checking each school's own score policy (ACT superscore FAQ, 2026).
- The ACT test is $70; the science add-on $5 and the writing add-on $25, or $100 for all three; late registration $42, standby testing $75, each additional score report $20 (ACT, 2026).
- Four answer choices in every section, including math, which had five before the enhanced test. Paper, online at a test center, or on your own device, with seven national Saturday dates a year. Up to 12 attempts, though ACT suggests most students retest two to three times. Multiple-choice scores in two to eight weeks, five to eight with writing (ACT, 2026).
- National ranks, the percent of recent ACT-tested graduates at or below each score, for tests taken September 2026 through August 2027 (graduates of 2024, 2025 and 2026). Composite: 36 is 100, 34 is 99, 32 is 97, 30 is 94, 28 is 91, 27 is 89, 26 is 86, 24 is 80, 22 is 72, 20 is 63, 18 is 52, 16 is 41; mean 19.1, standard deviation 6.1. By section at 30: English 93, math 95, reading 89, science 95; at 25: 84, 84, 78, 86; at 20: 64, 68, 56, 60. Section means: English 18.4, math 19.0, reading 20.0, science 19.5 (ACT national ranks, 2026).

## Post file format
`src/blog/<slug>.html`: an HTML comment front-matter block with JSON metadata, then the body.
Allowed body tags: h2, h3, p, ul, ol, li, div.tablewrap > table (thead/tbody/tr/th/td), strong, em, a. No h1, images, scripts, or inline styles.

## Answer engine visibility (GEO)
AI assistants quote pages that answer cleanly, and they cite third-party mentions more than brand homepages. Rules that follow from this:
- Every post's first 80 words must stand alone as a quotable answer with the key number in it.
- One-sentence definitions for any term of art (an assistant lifts definitional sentences verbatim).
- Keep facts identical everywhere they appear on the site; contradictions kill entity trust.
- Comparison and "what is a good X" pages earn the most AI citations; keep them current (date in title, yearly refresh).
- Third-party mentions matter more than backlinks for AI answers: pursue them via the partnerships in GROWTH.md, never via fake reviews or planted content.

## Bylines, categories, dates, outbound links (v2)
- Authors are pen names of the SFN editorial team: Maya Chen, Sarah Whitfield, Elena Rodriguez, Aisha Thompson, David Okafor, James Corbett (plus SFN Team for company news). Bylines only: never invent credentials, degrees, bios, or personal anecdotes presented as the author's lived experience.
- Categories now include Admissions (application timelines, essays, resumes, recommendations, waivers).
- Dates: published date = the date the post actually goes live. Future-dated posts are held by the generator until a deploy on or after that date. Never backdate.
- Every non-news post includes 1 to 3 outbound links to authoritative sources woven into sentences: mba.com, gmac.com, ets.org, official school pages (class profiles), or approved outlets. Link the page you are actually referencing. Never link banned sources.
- Admissions posts: no school-specific deadlines, policies, or statistics unless they are on the fact sheet; link the school's official page and describe in general terms instead.
