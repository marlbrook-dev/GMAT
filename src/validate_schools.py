"""Schema and source-policy validator for the school library.

Called by build_rankings.py before anything is computed. Hard failures stop
the build; soft warnings (weak sources queued for replacement) are printed.
Policy source: CLAUDE.md. Every published figure needs src, year, and url;
unverifiable values are null, never guesses; GMAT editions are never mixed
or converted.
"""
import sys

REGIONS = {"Northeast", "Midwest", "South", "West"}
TYPES = {"Private", "Public"}

# Fatal: these may never appear as a source (CLAUDE.md banned list).
BANNED_SOURCES = ["gmat club", "gmatclub", "quora", "wikipedia", "gyandhan",
                  "pagalguy", "reddit", "forum"]
# Warned: allowed for now, queued for replacement with official pages.
WEAK_SOURCES = ["clear admit", "stacy blackman", "search snippet", "f1gmat", "leland"]

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
    if warnings:
        print(f"validate_schools: {weak_count} figures still on weak sources "
              f"(Clear Admit / Stacy Blackman / snippets), replacement queued", file=sys.stderr)
    if errors:
        for e in errors[:40]:
            print("validate_schools ERROR:", e, file=sys.stderr)
        print(f"validate_schools: {len(errors)} error(s)", file=sys.stderr)
        sys.exit(1)
    return warnings
