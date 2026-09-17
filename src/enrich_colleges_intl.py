"""Add international enrolment share to the college files from College Scorecard.

Why this exists: the international hub had nothing for undergraduates, and the obvious
sources for the undergraduate story (SEVIS fees, F-1 process, OPT rules on uscis.gov,
dhs.gov, travel.state.gov) are all blocked from this environment by egress policy. Rather
than write those figures from memory, which the house rules forbid, this adds the one
international fact that IS reachable and authoritative: the share of a college's students
who are non-resident aliens, as the US Department of Education publishes it.

The field is race_ethnicity.non_resident_alien in the Scorecard institution data. It is a
share of enrolment, not a headcount, and it counts non-resident aliens rather than "visa
holders", so it is stored under a name that says what it is and the page wording follows
the source rather than improving on it.

Run:  python3 src/enrich_colleges_intl.py
"""
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "data" / "colleges"
KEY = "GIwouLRLS079WaXL9CG6vNBT9ch6qKvgmAOWZFdG"
FIELD = "latest.student.demographics.race_ethnicity.non_resident_alien"
API = "https://api.data.gov/ed/collegescorecard/v1/schools"
BATCH = 80


def fetch(ids):
    q = urllib.parse.urlencode({"api_key": KEY, "id": ",".join(ids),
                                "_per_page": 100, "_fields": "id," + FIELD})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(API + "?" + q, timeout=90) as r:
                return json.load(r).get("results", [])
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt * 2)
                continue
            raise SystemExit("Scorecard returned %s. Stopping rather than writing partial "
                             "data: a half enriched set would look complete." % e.code)
        except Exception:
            if attempt < 3:
                time.sleep(2 ** attempt * 2)
                continue
            raise
    return []


def main():
    files = sorted(DATA.glob("*.json"))
    by_id = {}
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("unitid"):
            by_id.setdefault(str(d["unitid"]), []).append((f, d))
    ids = sorted(by_id)
    print("fetching international share for %d colleges" % len(ids))
    values = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        for row in fetch(chunk):
            v = row.get(FIELD)
            if isinstance(v, (int, float)):
                values[str(row.get("id"))] = v
        sys.stdout.write("\r  %d/%d" % (min(i + BATCH, len(ids)), len(ids)))
        sys.stdout.flush()
    print()

    written = skipped = 0
    for uid, entries in by_id.items():
        v = values.get(uid)
        for f, d in entries:
            prof = d.setdefault("profile", {})
            if v is None:
                # No value is recorded as no value. The page shows a dash.
                prof.pop("intl_share_pct", None)
                skipped += 1
                continue
            prof["intl_share_pct"] = {
                "v": round(v * 100, 1),
                "stat": "share of enrolment reported as non-resident alien",
                "src": "US Department of Education, College Scorecard",
                "year": 2026,
                "url": d.get("scorecard") or
                       "https://collegescorecard.ed.gov/school/?%s" % uid,
                "release": "Most Recent Cohorts institution file",
            }
            f.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            written += 1
    print("wrote %d colleges, %d had no value and keep a dash" % (written, skipped))
    if written:
        vals = sorted(((v, u) for u, v in values.items()), reverse=True)[:8]
        print("highest shares found:")
        for v, u in vals:
            name = by_id[u][0][1]["name"]
            print("   %-46s %.1f%%" % (name[:46], v * 100))


if __name__ == "__main__":
    main()
