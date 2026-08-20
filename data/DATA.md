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
