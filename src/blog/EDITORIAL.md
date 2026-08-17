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

Product facts (the only permitted product claims):
- Start From Nowhere is an adaptive GMAT Focus trainer: 180 original practice items across Quant, Verbal, and Data Insights; a rating per skill keyed to the official score-report skill labels; misses return on a spaced schedule; timing tracked per question. First round free, no account needed.

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
