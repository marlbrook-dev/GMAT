# School Data Research Protocol (startfromnowhere.com rankings library)

You are verifying and filling official data for US full-time MBA programs. Your batch file lists five schools with their CURRENT data. For each school, fill gaps and replace weak sources with the school's OWN official pages.

## Network
Use WebSearch and WebFetch. Outbound HTTPS works. If a page will not load, record it under `_failures` and move on. NEVER substitute memory, cached knowledge, or a non-official source for a figure. Fetch PDFs only if WebFetch handles them; otherwise note the PDF URL in `_failures`.

## Fields per school
class_year, gmat_focus, gmat_classic, gre_quant, gre_verbal, gpa, accept_rate_pct, class_size, work_exp_years, women_pct, intl_pct, tuition_usd, salary_median_usd, employment_rate_pct.

## Hard source rules
1. Only report a figure you actually read on a page you fetched in this session. Record the exact URL you fetched in `url`.
2. Preferred and only source for this pass: the school's own official pages (their .edu or program domain): class profile / admissions statistics page; for salary_median_usd and employment_rate_pct the school's official employment report; for tuition_usd the school's official cost of attendance or tuition page.
3. If the school does not publish a figure on an official page you can reach, list the field name under `_null` with a short reason in `_notes`. Do not fall back to third parties.
4. BANNED, never cite and never open for data: GMAT Club, Quora, Wikipedia, GyanDhan, Pagalguy, Reddit, any forum, and coaching or admissions-consulting blogs (Clear Admit, Stacy Blackman, F1GMAT, Leland, Menlo Coaching, Accepted, and similar).
5. GMAT editions: gmat_focus is GMAT Focus Edition (205 to 805). gmat_classic is the old 200 to 800 exam. NEVER convert between editions. Only classify a figure as Focus if the page labels it Focus, or the profile is Class of 2026 or later AND the value is consistent with the Focus scale as labeled. If ambiguous, leave both unset and explain in `_notes`.
6. `stat` records exactly what the page says: "average", "median", "mid-80% 655-735", and for employment_rate_pct the definition, e.g. "accepted offers within 3 months of graduation"; for salary "median base salary".
7. tuition_usd: annual tuition for the current academic year, tuition only, excluding fees and living costs when the page itemizes them. `stat` notes the academic year, e.g. "2025-26 rate". `year` is the first calendar year of that academic year.
8. `year` is always an integer (the publication or class profile year). `src` is a short human label like "Haas MBA class profile" or "Fuqua employment report".

## Method per school
1. WebSearch variants: "<name> MBA class profile", "<name> MBA class of 2026 profile site:<domain>", "<name> MBA employment report", "<name> MBA tuition cost of attendance".
2. WebFetch the official pages; extract every field visible, with its exact wording for `stat`.
3. The batch file shows current data. Keep any figure already sourced to the school's own domain (just add the missing `year` if you can confirm it from the page). Replace anything sourced to Clear Admit, Stacy Blackman, "search snippets", F1GMAT, Leland, or Poets and Quants when an official figure exists. Fill nulls.

## Output
Write ONE file: the result path given in your task message. Content: a single JSON object, keyed by slug:

{
  "<slug>": {
    "class_year": "Class of 2026",
    "gmat_focus": {"v": 655, "stat": "average", "src": "...", "year": 2025, "url": "https://..."},
    "...": "only include fields you verified THIS session; omit fields you did not check",
    "_null": ["accept_rate_pct"],
    "_notes": "short notes on definitions or ambiguities",
    "_failures": ["https://url-that-would-not-load"]
  }
}

Rules for the file: valid JSON, no comments, no em or en dashes anywhere in strings, plain ASCII where possible. Your final chat reply should be one line per school: slug, number of fields verified, number null, any blockers. Do not paste the JSON into the chat.
