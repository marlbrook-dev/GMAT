"""Provenance and plausibility checks for data/colleges/.

Same contract as validate_schools.py: every published figure carries a source, a
year and a URL, and anything outside a plausible range is treated as a data entry
error rather than published. The college library is machine extracted from one
federal file, so the interesting failures are different from the MBA library's:
not a banned source, but a unit slip (a rate stored as 0.93 instead of 93) or a
field that silently stopped being populated in a new release.
"""
import sys

# field: (low, high, label)
RANGES = {
    "admit_rate_pct": (0.1, 100.0, "admission rate"),
    "sat_avg": (400, 1600, "SAT average"),
    "sat_reading_mid": (100, 800, "SAT reading midpoint"),
    "sat_math_mid": (100, 800, "SAT math midpoint"),
    "act_mid": (1, 36, "ACT midpoint"),
    "undergrads": (1, 200000, "undergraduate enrollment"),
    "net_price_usd": (0, 120000, "net price"),
    "cost_attendance_usd": (1000, 150000, "cost of attendance"),
    "tuition_in_state_usd": (0, 120000, "in-state tuition"),
    "tuition_out_state_usd": (0, 120000, "out-of-state tuition"),
    "grad_rate_6yr_pct": (0.0, 100.0, "graduation rate"),
    "retention_pct": (0.0, 100.0, "retention rate"),
    "earnings_10yr_usd": (5000, 400000, "earnings"),
    "median_debt_usd": (0, 300000, "median debt"),
    "pell_pct": (0.0, 100.0, "Pell share"),
    "federal_loan_pct": (0.0, 100.0, "federal loan share"),
}
NUMERIC = set(RANGES)


def validate(colleges):
    errs, warns = [], []
    slugs = set()
    for c in colleges:
        slug = c.get("slug")
        if not slug:
            errs.append("a college file has no slug")
            continue
        if slug in slugs:
            errs.append("%s: duplicate slug" % slug)
        slugs.add(slug)
        for key in ("name", "state", "unitid", "scorecard"):
            if not c.get(key):
                errs.append("%s: missing %s" % (slug, key))
        prof = c.get("profile") or {}
        for name, f in prof.items():
            v = f.get("v")
            if v is None:
                # A null needs no provenance; that is the point of a null.
                continue
            for k in ("src", "year", "url"):
                if not f.get(k):
                    errs.append("%s: %s has a value but no %s" % (slug, name, k))
            if name in NUMERIC:
                if not isinstance(v, (int, float)):
                    errs.append("%s: %s is %r, not a number" % (slug, name, v))
                    continue
                lo, hi, label = RANGES[name]
                if not (lo <= v <= hi):
                    errs.append("%s: %s of %s is outside the plausible range %s to %s"
                                % (slug, label, v, lo, hi))
        # A rate stored as a fraction is the failure mode that looks fine in a table
        # and quietly ruins every percentile. Catch it explicitly.
        for name in ("grad_rate_6yr_pct", "retention_pct", "pell_pct", "admit_rate_pct"):
            v = (prof.get(name) or {}).get("v")
            if isinstance(v, (int, float)) and 0 < v <= 1.0:
                warns.append("%s: %s is %s, which looks like a fraction rather than a "
                             "percentage" % (slug, name, v))
    if warns:
        print("validate_colleges: %d warning(s)" % len(warns), file=sys.stderr)
        for w in warns[:10]:
            print("  warn: " + w, file=sys.stderr)
    if errs:
        print("validate_colleges: %d error(s)" % len(errs), file=sys.stderr)
        for e in errs[:25]:
            print("  " + e, file=sys.stderr)
        raise SystemExit("college data failed validation")
    return True
