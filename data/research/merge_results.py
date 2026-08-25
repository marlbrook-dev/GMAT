"""Merge school-research result JSON into data/schools/<slug>.json with policy checks.

Usage: python3 data/research/merge_results.py <result.json> [...]
Result shape: see data/research/PROTOCOL.md. Prints a review log of every
change; rejects fields that violate policy (missing source/year/url, weak or
banned sources, out-of-range values, program-total tuitions, em dashes).
Review the log before committing; judgment calls (one-year program totals,
undated official pages) are applied manually, never silently.
"""
import json, pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from validate_schools import RANGES, BANNED_SOURCES, WEAK_SOURCES

FIELDS = ["gmat_focus", "gmat_classic", "gre_quant", "gre_verbal", "gpa",
          "accept_rate_pct", "class_size", "work_exp_years", "women_pct",
          "intl_pct", "tuition_usd", "salary_median_usd", "employment_rate_pct"]

def load_result(path):
    text = pathlib.Path(path).read_text().strip()
    text = re.sub(r"^```(json)?|```$", "", text, flags=re.M).strip()
    return json.loads(text)

def weak(src):
    s = str(src or "").lower()
    return any(w in s for w in WEAK_SOURCES)

def banned(src):
    s = str(src or "").lower()
    return any(b in s for b in BANNED_SOURCES)

def fmtv(f):
    if not f or f.get("v") is None:
        return "null"
    return f"{f['v']} ({f.get('src','?')}, {f.get('year','?')})"

changed = kept = rejected = nulled = 0
for arg in sys.argv[1:]:
    try:
        res = load_result(arg)
    except Exception as e:
        print(f"REJECT FILE {arg}: {e}")
        continue
    for slug, upd in res.items():
        p = REPO / "data" / "schools" / f"{slug}.json"
        if not p.exists():
            print(f"REJECT {slug}: no such school file")
            continue
        s = json.loads(p.read_text())
        prof = s.setdefault("profile", {})
        if isinstance(upd.get("class_year"), str) and upd["class_year"].strip():
            if prof.get("class_year") != upd["class_year"]:
                print(f"{slug}.class_year: {prof.get('class_year')!r} -> {upd['class_year']!r}")
            prof["class_year"] = upd["class_year"]
        for f in FIELDS:
            nf = upd.get(f)
            if not isinstance(nf, dict):
                continue
            v = nf.get("v")
            if v is None:
                continue
            problems = []
            meta = (str(nf.get("stat", "")) + " " + str(nf.get("note", ""))).lower()
            if f == "tuition_usd" and any(t in meta for t in ["program total", "total program", "not per year", "not annual", "two-year total", "16-month", "program cost"]):
                problems.append("tuition is a program total, not annual")
            if nf.get("note") and not problems:
                nf["stat"] = (str(nf.get("stat") or "").strip() + ("; " if nf.get("stat") else "") + str(nf["note"]).strip())[:300]
            if not nf.get("src"): problems.append("no src")
            if not isinstance(nf.get("year"), int) or not (2018 <= nf["year"] <= 2027): problems.append("bad year")
            if not str(nf.get("url", "")).startswith("http"): problems.append("no url")
            if banned(nf.get("src")) or weak(nf.get("src")): problems.append("disallowed source")
            lo_hi = RANGES.get(f)
            if lo_hi and isinstance(v, (int, float)) and not (lo_hi[0] <= v <= lo_hi[1]): problems.append(f"out of range {lo_hi}")
            if "—" in json.dumps(nf) or "–" in json.dumps(nf): problems.append("em dash")
            if problems:
                print(f"REJECT {slug}.{f}: {problems} :: {nf}")
                rejected += 1
                continue
            old = prof.get(f)
            new = {k: nf[k] for k in ["v", "stat", "src", "year", "url"] if nf.get(k) is not None}
            old_v = (old or {}).get("v")
            if old_v is not None and old_v != v:
                print(f"{slug}.{f}: VALUE CHANGE {fmtv(old)} -> {fmtv(new)}")
            elif old_v is None:
                print(f"{slug}.{f}: filled {fmtv(new)}")
            else:
                print(f"{slug}.{f}: re-sourced -> {new.get('src')}, {new.get('year')}")
            prof[f] = new
            changed += 1
        for f in upd.get("_null") or []:
            old = prof.get(f)
            if not isinstance(old, dict) or old.get("v") is None:
                continue
            # official page does not publish it: drop weak/yearless values, keep sourced publisher data
            if weak(old.get("src")) or not old.get("year"):
                print(f"{slug}.{f}: NULLED (not published officially; old was {fmtv(old)})")
                prof[f] = {"v": None}
                nulled += 1
            else:
                print(f"{slug}.{f}: kept publisher figure {fmtv(old)} (school does not publish)")
                kept += 1
        notes = (upd.get("_notes") or "").strip()
        if notes:
            base = (s.get("notes") or "").strip()
            if notes not in base:
                s["notes"] = (base + (" " if base else "") + notes).strip()
        p.write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n")
print(f"\nmerged: {changed} fields set, {nulled} nulled, {kept} kept, {rejected} rejected")
