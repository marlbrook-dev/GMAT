"""Attach federal earnings and debt to the MBA library.

The MBA school pages report the salary each school publishes in its own employment
report. That figure is real but it is the school's own: it covers the graduates who
responded, in the year the school chose, on a definition the school set.

The College Scorecard's field of study file reports something different and
independent: median earnings and median federal debt for people who completed a
master's in Business Administration (CIP 5202) at that institution, from tax and
federal aid records rather than a survey. Having both lets a reader see where they
agree and where they do not, which is more useful than either alone.

This does NOT feed the SFN Score. It is reported alongside it, with its coverage.

Coverage is the whole story with this dataset. Federal earnings cover only people
whose records the government holds, which means federal aid recipients, and at a
school with large need based scholarships and many international students that is a
small and unrepresentative slice. Harvard's figure rests on 107 people out of about
877 graduates and lands at 103k against the 184.5k the school reports; Wharton's
rests on 381 and lands at 210k. The figures are not wrong, they are answering a
narrower question, so the number of people behind each one is stored and shown
beside it, and a figure resting on under forty percent of the class is flagged.

Matching is by institution name and is deliberately strict. The federal file lists
"University of Kent" and "University of Missouri-Kansas City"; a prefix match would
have attached the first to Kentucky and the second to Trulaske, publishing a wrong
number on a school page, which is the exact failure the source rules exist to
prevent. So every campus-suffixed name below was checked by hand, and a school with
no confident match gets nothing rather than a guess.

Usage:
    python3 src/enrich_schools_federal.py path/to/Most-Recent-Cohorts-Field-of-Study.csv
"""
import csv
import json
import pathlib
import re
import sys

D = pathlib.Path(__file__).parent
SCHOOLS = D.parent / "data" / "schools"

SRC = "US Department of Education, College Scorecard field of study file"
RELEASE = "2026 release, Most Recent Cohorts field of study file"
YEAR = 2026
MISSING = {"", "NA", "NULL", "PS", "PrivacySuppressed"}
CIP_MBA = "5202"
CRED_MASTERS = "5"

# Hand verified. Each maps our university name to the exact INSTNM in the federal
# file, after checking that the campus is the one the business school sits on.
ALIASES = {
    "Arizona State University": "Arizona State University Campus Immersion",
    "University at Buffalo SUNY": "University at Buffalo",
    "University of Cincinnati": "University of Cincinnati-Main Campus",
    "Columbia University": "Columbia University in the City of New York",
    "Georgia Institute of Technology": "Georgia Institute of Technology-Main Campus",
    "University of Michigan": "University of Michigan-Ann Arbor",
    "North Carolina State University": "North Carolina State University at Raleigh",
    "Ohio State University": "Ohio State University-Main Campus",
    "University of Oklahoma": "University of Oklahoma-Norman Campus",
    "Pennsylvania State University": "Pennsylvania State University-Main Campus",
    "University of Pittsburgh": "University of Pittsburgh-Pittsburgh Campus",
    "Purdue University": "Purdue University-Main Campus",
    "University of South Carolina": "University of South Carolina-Columbia",
    "Texas A&M University": "Texas A&M University-College Station",
    "Tulane University": "Tulane University of Louisiana",
    "University of Virginia": "University of Virginia-Main Campus",
    "University of Washington": "University of Washington-Seattle Campus",
    "College of William & Mary": "William & Mary",
}

# Checked and genuinely absent from the federal MBA file, or ambiguous across
# campuses. Recorded here so a future run does not mistake them for an oversight.
NO_FEDERAL_RECORD = {
    "Indiana University Bloomington": "no CIP 5202 master's record in the federal file",
    "University of Kentucky": "no CIP 5202 master's record in the federal file",
    "University of Louisville": "no CIP 5202 master's record in the federal file",
    "Massachusetts Institute of Technology": "no CIP 5202 master's record in the federal file",
    "University of Missouri": "no CIP 5202 master's record in the federal file",
    "Rutgers University": "the business school spans the Newark and New Brunswick "
                          "campuses, which report separately, so neither record "
                          "describes the program on its own",
}


def norm(s):
    s = (s or "").lower().replace("&", "and")
    s = re.sub(r"\b(the|at|of|in)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def val(row, key):
    v = (row.get(key) or "").strip()
    return None if v in MISSING else v


def money(row, key):
    v = val(row, key)
    try:
        return int(float(v)) if v is not None else None
    except (TypeError, ValueError):
        return None


def main(path):
    fed = {}
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row.get("CIPCODE") == CIP_MBA and row.get("CREDLEV") == CRED_MASTERS:
                fed[norm(row["INSTNM"])] = row

    files = sorted(SCHOOLS.glob("*.json"))
    attached, absent, unmatched = 0, 0, []
    for p in files:
        s = json.loads(p.read_text(encoding="utf-8"))
        uni = s.get("university") or ""
        target = ALIASES.get(uni, uni)
        row = fed.get(norm(target))
        if row is None:
            if uni in NO_FEDERAL_RECORD:
                s["federal"] = {"matched": False, "reason": NO_FEDERAL_RECORD[uni]}
                absent += 1
            else:
                unmatched.append((s["slug"], uni))
                s.pop("federal", None)
        else:
            def f(v):
                return ({"v": v, "src": SRC, "year": YEAR, "url": s.get("website") or "",
                         "release": RELEASE, "instnm": row["INSTNM"]}
                        if v is not None else {"v": None})
            earn_n = money(row, "EARN_COUNT_WNE_1YR")
            # IPEDSCOUNT is not a usable denominator: it reports 8 completers for Rice
            # and 11 for Booth, which would make their coverage several thousand
            # percent. Our own class_size is sourced from the school's published class
            # profile and is validated, so the flag is computed against that instead.
            # Even then a ratio is not published, because the federal earnings cohort
            # pools more than one graduating year and can legitimately exceed one
            # class. The count is published; the flag only marks the cases where the
            # figure clearly rests on a small minority of the class.
            cls = ((s.get("profile") or {}).get("class_size") or {}).get("v")
            low = bool(earn_n and cls and earn_n < 0.4 * cls)
            s["federal"] = {
                "matched": True,
                "instnm": row["INSTNM"],
                "earn_1yr_usd": f(money(row, "EARN_MDN_1YR")),
                "earn_4yr_usd": f(money(row, "EARN_MDN_4YR")),
                "debt_median_usd": f(money(row, "DEBT_ALL_STGP_EVAL_MDN")),
                "national_earn_4yr_usd": f(money(row, "EARN_MDN_4YR_NAT")),
                # How many people the earnings figure actually rests on, and how that
                # compares with the graduating class. Without these the number reads as
                # "the MBA salary" when it is "the salary of the aid receiving minority".
                "earn_n": earn_n,
                "low_coverage": low,
            }
            attached += 1
        p.write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print("federal MBA data: attached to %d schools, %d recorded as having no federal "
          "record" % (attached, absent))
    if unmatched:
        print("  UNMATCHED (add an alias or a NO_FEDERAL_RECORD entry):")
        for slug, uni in unmatched:
            print("    %-30s %s" % (slug, uni))
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
