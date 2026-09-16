"""The SFN College Score.

What it measures, and why those things.

Most undergraduate rankings weight reputation surveys and per student spending.
Both reward being rich and being old, and one of them, selectivity, rewards a
school for turning more people away. A school that rejects 95 percent of
applicants has not taught anybody anything yet.

So this score uses only outcomes, all from one official federal source, and leaves
selectivity out on purpose:

  Completion        30   does the school actually get students through
                         (6 year graduation 20, first year retention 10)
  Earnings          25   median earnings 10 years after entry
  Cost and debt     25   net price 15, debt against earnings 10
  Access            20   share of students on Pell grants

Admission rate, test scores, sticker price and endowment are REPORTED on every
school page, because an applicant needs them, and are never scored.

Each component is a percentile rank within the schools that report it, so the
score is explicitly relative to the 1400 or so four year nonprofit institutions in
the library, not an absolute quality measure. Weights are renormalised over the
components a school actually reports, and a school needs at least three of the four
to be ranked at all; the rest are listed unscored rather than guessed at.
"""

WEIGHTS = {"completion": 0.30, "earnings": 0.25, "cost": 0.25, "access": 0.20}

# A school is ranked only if it reports BOTH headline outcomes. Allowing a school to
# be ranked on the other components alone put a medical centre with no graduation rate
# and a seminary with no earnings figure into the top five, each of them scoring well
# precisely because the demanding components were missing. A ranking about whether
# students finish and what they earn cannot rank a school that reports neither.
REQUIRED = ("completion", "earnings")
MIN_COMPONENTS = 3


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

    net = field(s, "net_price_usd")
    ratio = debt_ratio(s)
    parts, wts = [], []
    if net is not None:
        # Lower net price is better, so the rank is inverted.
        parts.append(pct_rank(dist["net_price_usd"], net, higher_is_better=False))
        wts.append(1.5)
    if ratio is not None:
        parts.append(pct_rank(dist["debt_ratio"], ratio, higher_is_better=False))
        wts.append(1.0)
    if parts:
        out["cost"] = sum(p * w for p, w in zip(parts, wts)) / sum(wts)

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
        (scored if sc is not None else unscored).append(s)
    scored.sort(key=lambda x: (-x["sfn_score"], x["name"]))
    for i, s in enumerate(scored, 1):
        s["sfn_rank"] = i
    for s in unscored:
        s["sfn_rank"] = None
        s["unranked_reason"] = unranked_reason(s, s.get("sfn_components") or {})
    return scored, unscored
