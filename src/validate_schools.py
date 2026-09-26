"""Schema and source-policy validator for the school library.

Called by build_rankings.py before anything is computed. Hard failures stop
the build; soft warnings (weak sources queued for replacement) are printed.
Policy source: CLAUDE.md. Every published figure needs src, year, and url;
unverifiable values are null, never guesses; GMAT editions are never mixed
or converted.
"""
import re
import sys

REGIONS = {"Northeast", "Midwest", "South", "West"}
TYPES = {"Private", "Public"}

# The source policy lives in src/sources.py so the three published corpora
# (schools, colleges, exams) cannot drift apart on what counts as a bad source.
# Re-exported here because data/research/merge_results.py imports both names
# from this module.
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sources import BANNED_SOURCES, WEAK_SOURCES  # noqa: E402,F401

RANGES = {
    "gmat_focus": (205, 805), "gmat_classic": (200, 800),
    "gre_quant": (130, 170), "gre_verbal": (130, 170),
    "gpa": (2.5, 4.0), "accept_rate_pct": (0, 100),
    "class_size": (10, 2000), "work_exp_years": (0, 15),
    "women_pct": (0, 100), "intl_pct": (0, 100),
    "tuition_usd": (10000, 150000), "salary_median_usd": (40000, 300000),
    "employment_rate_pct": (0, 100),
}

RANK_KEYS = {"usnews", "ft", "bloomberg", "qs", "pq"}


def validate(schools):
    errors, warnings = [], []
    seen = set()
    weak_count = 0
    for s in schools:
        slug = s.get("slug") or "?"
        if slug in seen:
            errors.append(f"{slug}: duplicate slug")
        seen.add(slug)
        for key in ["slug", "name", "university", "city", "state", "region", "type", "ranks", "profile"]:
            if key not in s:
                errors.append(f"{slug}: missing key {key}")
        if s.get("region") not in REGIONS:
            errors.append(f"{slug}: bad region {s.get('region')!r}")
        if s.get("type") not in TYPES:
            errors.append(f"{slug}: bad type {s.get('type')!r}")
        for k, r in (s.get("ranks") or {}).items():
            if k not in RANK_KEYS:
                errors.append(f"{slug}: unknown rank source {k}")
            if r and r.get("rank") is not None and not (1 <= r["rank"] <= 200):
                errors.append(f"{slug}: implausible {k} rank {r['rank']}")
        for f, fv in (s.get("profile") or {}).items():
            if not isinstance(fv, dict):
                if f == "class_year":
                    continue
                errors.append(f"{slug}.{f}: not an object")
                continue
            v = fv.get("v")
            if v is None:
                continue
            for req in ["src", "year"]:
                if not fv.get(req):
                    errors.append(f"{slug}.{f}: published value without {req}")
            if not fv.get("url", "").startswith("http"):
                errors.append(f"{slug}.{f}: published value without a source url")
            if not isinstance(fv.get("year"), int) or not (2018 <= fv["year"] <= 2027):
                errors.append(f"{slug}.{f}: implausible source year {fv.get('year')!r}")
            src = str(fv.get("src", "")).lower()
            if any(b in src for b in BANNED_SOURCES):
                errors.append(f"{slug}.{f}: banned source {fv.get('src')!r}")
            if any(w in src for w in WEAK_SOURCES):
                weak_count += 1
                warnings.append(f"{slug}.{f}: weak source {fv.get('src')!r}")
            lo_hi = RANGES.get(f)
            if lo_hi and isinstance(v, (int, float)) and not (lo_hi[0] <= v <= lo_hi[1]):
                errors.append(f"{slug}.{f}: value {v} outside plausible range {lo_hi}")
            for sval in [fv.get("src"), fv.get("stat"), fv.get("url")]:
                if isinstance(sval, str) and ("—" in sval or "–" in sval):
                    errors.append(f"{slug}.{f}: em/en dash in metadata")
        # official_hosts: places outside the school's own domain where the school itself
        # publishes (its storage bucket, an alias domain). Each needs the evidence that it is
        # the school's and the date that was checked, because this field changes a figure's
        # label from secondary to official and must not be a way to launder a publisher.
        for oh in (s.get("official_hosts") or []):
            if not (isinstance(oh, dict) and str(oh.get("prefix", "")).startswith("https://")
                    and oh.get("evidence") and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(oh.get("checked", "")))):
                errors.append(f"{slug}.official_hosts: each entry needs an https prefix, evidence and a checked date")
            elif any(b in str(oh.get("prefix", "")).lower() for b in ("poetsandquants", "usnews", "gmac.com", "bloomberg", "ft.com", "topuniversities", "businessbecause")):
                errors.append(f"{slug}.official_hosts: {oh.get('prefix')} is a publisher, not the school")
        # Scholarship block. Same provenance rules as every other figure, plus a checked
        # date, because award terms change every admissions cycle and a 2024 number quoted
        # in 2026 is misinformation even when it was true when written.
        sch = s.get("scholarship")
        if sch is not None:
            if not isinstance(sch, dict):
                errors.append(f"{slug}.scholarship: not an object")
            else:
                checked = sch.get("checked")
                if not (isinstance(checked, str) and len(checked) == 10 and checked[4] == "-"):
                    errors.append(f"{slug}.scholarship: missing or malformed checked date "
                                  f"{checked!r} (want YYYY-MM-DD)")
                review = sch.get("review")
                if review is not None and review.get("v") not in ("automatic", "separate"):
                    errors.append(f"{slug}.scholarship.review: value must be 'automatic' or "
                                  f"'separate', got {review.get('v')!r}")
                for f in ("review", "pct_receiving", "avg_award_usd"):
                    fv = sch.get(f)
                    if fv is None:
                        continue
                    if not isinstance(fv, dict):
                        errors.append(f"{slug}.scholarship.{f}: not an object")
                        continue
                    if fv.get("v") is None:
                        continue
                    for req in ("src", "year", "stat"):
                        if not fv.get(req):
                            errors.append(f"{slug}.scholarship.{f}: published value without {req}")
                    if not str(fv.get("url", "")).startswith("http"):
                        errors.append(f"{slug}.scholarship.{f}: published value without a source url")
                    src = str(fv.get("src", "")).lower()
                    if any(b in src for b in BANNED_SOURCES):
                        errors.append(f"{slug}.scholarship.{f}: banned source {fv.get('src')!r}")
                    for sval in (fv.get("src"), fv.get("stat"), fv.get("url")):
                        if isinstance(sval, str) and ("\u2014" in sval or "\u2013" in sval):
                            errors.append(f"{slug}.scholarship.{f}: em/en dash in metadata")
                pct = sch.get("pct_receiving")
                if pct and isinstance(pct.get("v"), (int, float)) and not (0 <= pct["v"] <= 100):
                    errors.append(f"{slug}.scholarship.pct_receiving: {pct['v']} is not a percentage")
                amt = sch.get("avg_award_usd")
                if amt and isinstance(amt.get("v"), (int, float)) and not (1000 <= amt["v"] <= 250000):
                    errors.append(f"{slug}.scholarship.avg_award_usd: {amt['v']} outside a plausible "
                                  f"annual award range")

    if warnings:
        print(f"validate_schools: {weak_count} figures still on weak sources "
              f"(Clear Admit / Stacy Blackman / snippets), replacement queued", file=sys.stderr)
    if errors:
        for e in errors[:40]:
            print("validate_schools ERROR:", e, file=sys.stderr)
        print(f"validate_schools: {len(errors)} error(s)", file=sys.stderr)
        sys.exit(1)
    return warnings
