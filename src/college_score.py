"""The SFN College Score.

What it measures, and why those things.

Most undergraduate rankings weight reputation surveys and per student spending.
Both reward being rich and being old, and one of them, selectivity, rewards a
school for turning more people away. A school that rejects 95 percent of
applicants has not taught anybody anything yet.

So this score uses only outcomes, all from one official federal source, and leaves
selectivity out on purpose:

  Completion        50   does the school actually get students through
                         (6 year graduation 2 parts, first year retention 1 part)
  Earnings          40   median earnings 10 years after entry
  Access            10   share of students on Pell grants

Admission rate, test scores, net price, debt and endowment are REPORTED on every
school page, because an applicant needs them, and are never scored.

Why price is not scored
-----------------------
It used to be. Net price was 15 percent of the score and debt against earnings
another 10, with Pell share at 20 on top, so 45 percent of the score measured what a
school charged and who it enrolled rather than what it did for them. The result was a
table headed by CUNY Baruch, seven University of California campuses and four Cal
State campuses, with Harvard, Yale, MIT and Chicago outside the top twenty. That is
not an unconventional ranking, it is an affordability index wearing a quality
ranking's clothes, and price was doing the work.

A price is an input, not an outcome. What a school charges belongs on its page, where
an applicant can weigh it against everything else, not inside a score that claims to
say how well the school educates people. Net price, median debt, in-state and
out-of-state tuition and the non-resident premium are all still published on every
college page and in the table. None of them touch the score.

Access stays, at 10 rather than 20. A school that admits only students who arrive
already advantaged and then posts good outcomes has done less work than one that
starts further back and gets to the same place, and Pell share is the only measure of
that in the federal data. At 20 it dominated; at 10 it informs.

How this was checked
--------------------
Weights that produce a plausible looking table are easy to write and hard to trust,
so src/validate_ranking.py compares our list against four published rankings that
disagree with each other: Times Higher Education on research and reputation, and
Washington Monthly on social mobility across its national, liberal arts and master's
categories. The old weighting put 44 percent of our top 25 in anybody's published top
25. This one puts 80 percent, and 96 percent of our top 25 appears somewhere in a
published ranking against 84 percent before.

The obvious failure mode of tuning against other people's lists is accidentally
rebuilding the selectivity ranking we refuse to build, because ranking by how hard a
school is to enter is the cheapest way to agree with everybody. The correlation
between this score and admission rate is -0.41, moderate rather than mechanical, and
25 of the top 100 are public institutions. Those two numbers are the guard; if either
moves sharply after a weight change, the change is wrong.
"""

WEIGHTS = {"completion": 0.50, "earnings": 0.40, "access": 0.10}

# A school is ranked only if it reports BOTH headline outcomes. Allowing a school to
# be ranked on the other components alone put a medical centre with no graduation rate
# and a seminary with no earnings figure into the top five, each of them scoring well
# precisely because the demanding components were missing. A ranking about whether
# students finish and what they earn cannot rank a school that reports neither.
REQUIRED = ("completion", "earnings")
# Two of the three components. Both required ones count, so this says: a school needs
# completion and earnings, and access is allowed to be missing.
MIN_COMPONENTS = 2


def field(school, name):
    return (school.get("profile", {}).get(name) or {}).get("v")


def pct_rank(sorted_vals, v, higher_is_better=True):
    """Percentile of v within sorted_vals, 0 to 100."""
    if not sorted_vals:
        return None
    lo, hi = 0, len(sorted_vals)
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_vals[mid] < v:
            lo = mid + 1
        else:
            hi = mid
    p = 100.0 * lo / max(len(sorted_vals) - 1, 1)
    p = max(0.0, min(100.0, p))
    return p if higher_is_better else 100.0 - p


def out_state_cost(s):
    """What a non-resident is charged, on one definition for every school.

    Net price is published for in-state students only, so it cannot answer the
    out-of-state question. Published out-of-state tuition and fees can, and it is the
    same measure for everyone: private tuition does not vary by residency, which was
    checked rather than assumed (all 872 private colleges in the library report
    identical in-state and out-of-state figures, while the public median premium is
    11,352 dollars). It is a sticker price rather than a post-aid price, so the two
    cost views answer different questions and are labelled separately, never blended.
    """
    return field(s, "tuition_out_state_usd")


def build_distributions(schools):
    """Collect the reported values for each metric so ranks are computed once."""
    keys = ["grad_rate_6yr_pct", "retention_pct", "earnings_10yr_usd",
            "net_price_usd", "pell_pct"]
    dist = {k: sorted(v for v in (field(s, k) for s in schools) if v is not None)
            for k in keys}
    ratios = []
    for s in schools:
        r = debt_ratio(s)
        if r is not None:
            ratios.append(r)
    dist["debt_ratio"] = sorted(ratios)
    dist["out_state_cost"] = sorted(
        v for v in (out_state_cost(s) for s in schools) if v is not None)
    return dist


def debt_ratio(s):
    """Median graduate debt as a share of median earnings ten years out.

    Debt on its own says nothing: 30k of debt against 100k of earnings is a
    different proposition from 30k against 35k. The ratio is what a borrower
    actually feels, and lower is better.
    """
    debt = field(s, "median_debt_usd")
    earn = field(s, "earnings_10yr_usd")
    if debt is None or not earn:
        return None
    return debt / float(earn)


def components(s, dist):
    """Each component as 0 to 100, or None where the school reports nothing."""
    out = {}

    grad = field(s, "grad_rate_6yr_pct")
    ret = field(s, "retention_pct")
    parts, wts = [], []
    if grad is not None:
        parts.append(pct_rank(dist["grad_rate_6yr_pct"], grad))
        wts.append(2.0)
    if ret is not None:
        parts.append(pct_rank(dist["retention_pct"], ret))
        wts.append(1.0)
    if parts:
        out["completion"] = sum(p * w for p, w in zip(parts, wts)) / sum(wts)

    earn = field(s, "earnings_10yr_usd")
    if earn is not None:
        out["earnings"] = pct_rank(dist["earnings_10yr_usd"], earn)

    # No cost component. Net price and the debt ratio are computed and published on
    # every college page, and both are deliberately absent from the score: see the
    # module docstring for what scoring them did to the table.

    pell = field(s, "pell_pct")
    if pell is not None:
        out["access"] = pct_rank(dist["pell_pct"], pell)

    return out


def unranked_reason(s, comps):
    """Why a school is listed but not ranked, in words a reader can check."""
    if s.get("health_special_focus"):
        return ("Special focus medical or health professions institution: its earnings "
                "reflect a mostly graduate professional student body, so it is not "
                "comparable with undergraduate programs.")
    missing = [k for k in REQUIRED if k not in comps]
    if missing:
        names = {"completion": "graduation and retention", "earnings": "earnings"}
        return ("The College Scorecard reports no %s data for this school."
                % " or ".join(names[m] for m in missing))
    return "Too few reported outcomes to score."


# There is deliberately no second, out-of-state SCORE here.
#
# The obvious way to build one is to swap net price for published out-of-state
# tuition, and it produces a table that looks plausible and is wrong: Caltech falls
# sixteen points and Princeton nearly fourteen, when neither charges a non-resident
# a different price. What moved was the measure, from post-aid net price to sticker
# tuition, not the residency. A column labelled "out of state" that mostly reranks
# private colleges by how much aid they give would mislead precisely the reader it
# claims to serve.
#
# The Scorecard publishes no out-of-state net price, so the honest out-of-state
# figure is the published tuition differential, which is reported as its own data
# point on the table and on every college page rather than folded into a score.

def score(s, dist):
    comps = components(s, dist)
    # Special focus health institutions are left unranked whatever they report.
    if s.get("health_special_focus"):
        return None, comps
    if any(k not in comps for k in REQUIRED) or len(comps) < MIN_COMPONENTS:
        return None, comps
    total = sum(WEIGHTS[k] * v for k, v in comps.items())
    wsum = sum(WEIGHTS[k] for k in comps)
    return round(total / wsum, 1), comps


def rank_all(schools):
    dist = build_distributions(schools)
    scored, unscored = [], []
    for s in schools:
        sc, comps = score(s, dist)
        s["sfn_score"] = sc
        s["sfn_components"] = {k: round(v, 1) for k, v in comps.items()}
        # What a non-resident actually pays extra, straight from two published
        # figures. No modelling: out-of-state tuition minus in-state tuition.
        ti, to = field(s, "tuition_in_state_usd"), field(s, "tuition_out_state_usd")
        s["out_state_premium"] = (to - ti) if (ti is not None and to is not None) else None
        (scored if sc is not None else unscored).append(s)
    scored.sort(key=lambda x: (-x["sfn_score"], x["name"]))
    for i, s in enumerate(scored, 1):
        s["sfn_rank"] = i
    for s in unscored:
        s["sfn_rank"] = None
        s["unranked_reason"] = unranked_reason(s, s.get("sfn_components") or {})
    return scored, unscored
