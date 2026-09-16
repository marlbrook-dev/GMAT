"""Build the undergraduate college library from the College Scorecard.

Source of truth is the US Department of Education's College Scorecard institution
file, which is the only national dataset that reports outcomes (completion,
earnings, debt, net price) on a common definition for every accredited institution.
Nothing here is typed from memory and nothing is inferred: a field the Scorecard
does not report is written as null with no source, and the site renders a dash.

Usage:
    python3 src/extract_colleges.py path/to/Most-Recent-Cohorts-Institution.csv

Writes one file per college into data/colleges/, matching the shape data/schools/
uses for MBA programs so the two libraries validate and render the same way.
"""
import csv
import json
import pathlib
import re
import sys

D = pathlib.Path(__file__).parent
OUT = D.parent / "data" / "colleges"

SRC = "US Department of Education, College Scorecard"
# The Scorecard publishes one institution file per release; every figure below comes
# from the release named here, and each school links to its own Scorecard page so a
# reader can check any number against the source.
RELEASE = "2026 release, Most Recent Cohorts institution file"
YEAR = 2026
DATA_URL = "https://collegescorecard.ed.gov/data/"

MISSING = {"", "NA", "NULL", "PS", "PrivacySuppressed"}

REGION = {
    "CT": "Northeast", "ME": "Northeast", "MA": "Northeast", "NH": "Northeast",
    "RI": "Northeast", "VT": "Northeast", "NJ": "Northeast", "NY": "Northeast",
    "PA": "Northeast",
    "IL": "Midwest", "IN": "Midwest", "MI": "Midwest", "OH": "Midwest",
    "WI": "Midwest", "IA": "Midwest", "KS": "Midwest", "MN": "Midwest",
    "MO": "Midwest", "NE": "Midwest", "ND": "Midwest", "SD": "Midwest",
    "DE": "South", "DC": "South", "FL": "South", "GA": "South", "MD": "South",
    "NC": "South", "SC": "South", "VA": "South", "WV": "South", "AL": "South",
    "KY": "South", "MS": "South", "TN": "South", "AR": "South", "LA": "South",
    "OK": "South", "TX": "South",
    "AZ": "West", "CO": "West", "ID": "West", "MT": "West", "NV": "West",
    "NM": "West", "UT": "West", "WY": "West", "AK": "West", "CA": "West",
    "HI": "West", "OR": "West", "WA": "West",
}
CONTROL = {"1": "Public", "2": "Private nonprofit"}
# Carnegie Basic classification. Special Focus institutions award a few bachelor's
# degrees alongside a mostly graduate professional mission, so their earnings reflect
# doctors and pharmacists rather than undergraduates. They stay in the library, with
# their own label, and are listed unranked.
CARNEGIE = {
    "15": "Doctoral, very high research", "16": "Doctoral, high research",
    "17": "Doctoral, professional", "18": "Master's, larger programs",
    "19": "Master's, medium programs", "20": "Master's, smaller programs",
    "21": "Baccalaureate, arts and sciences", "22": "Baccalaureate, diverse fields",
    "23": "Baccalaureate, associate's dominant", "24": "Baccalaureate and associate's",
    "25": "Special focus, faith related", "26": "Special focus, faith related",
    "27": "Special focus, medical school or center",
    "28": "Special focus, other health professions",
    "29": "Special focus, engineering", "30": "Special focus, technology",
    "31": "Special focus, business", "32": "Special focus, arts and design",
    "33": "Special focus, law",
}
SPECIAL_FOCUS_HEALTH = {"27", "28"}
# ADMCON7 records what the institution requires of applicants for admission.
TEST_POLICY = {
    "1": "Required",
    "2": "Recommended",
    "3": "Neither required nor recommended",
    "4": "Do not know",
    "5": "Considered but not required",
}


def val(row, key):
    v = (row.get(key) or "").strip()
    return None if v in MISSING else v


def num(row, key, cast=float, scale=1.0, nd=None):
    v = val(row, key)
    if v is None:
        return None
    try:
        x = cast(float(v) * scale)
    except (ValueError, TypeError):
        return None
    if nd is not None:
        x = round(x, nd)
    return x


def slugify(name, state):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    s = re.sub(r"-+", "-", s)
    return "%s-%s" % (s[:60].strip("-"), state.lower())


def field(v, url):
    """Every published figure carries its source, year, and a checkable URL."""
    if v is None:
        return {"v": None}
    return {"v": v, "src": SRC, "year": YEAR, "url": url, "release": RELEASE}


def clean_url(u):
    if not u:
        return None
    u = u.strip()
    if not u.lower().startswith(("http://", "https://")):
        u = "https://" + u
    return u


def main(path):
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    made, skipped = 0, 0
    seen = set()
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            # Currently operating, predominantly bachelor's degree granting, public or
            # private nonprofit. For profit institutions are excluded deliberately: their
            # outcomes are reported on the same basis but the sector's aid and completion
            # profile is different enough that mixing them into one ranking misleads.
            if row.get("CURROPER") != "1" or row.get("PREDDEG") != "3":
                skipped += 1
                continue
            if row.get("CONTROL") not in CONTROL:
                skipped += 1
                continue
            ug = num(row, "UGDS", int)
            if not ug or ug < 500:
                skipped += 1
                continue
            name = val(row, "INSTNM")
            state = val(row, "STABBR")
            unitid = val(row, "UNITID")
            if not name or not state or not unitid:
                skipped += 1
                continue
            slug = slugify(name, state)
            n = 2
            base = slug
            while slug in seen:
                slug = "%s-%d" % (base, n)
                n += 1
            seen.add(slug)

            # Each school's own Scorecard page, so any figure can be checked at source.
            page = "https://collegescorecard.ed.gov/school/?%s-%s" % (
                unitid, re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-"))
            public = row.get("CONTROL") == "1"
            rec = {
                "slug": slug,
                "unitid": int(unitid),
                "name": name,
                "city": val(row, "CITY"),
                "state": state,
                "region": REGION.get(state, "Other"),
                "type": CONTROL[row["CONTROL"]],
                "website": clean_url(val(row, "INSTURL")),
                "carnegie": CARNEGIE.get(val(row, "CCBASIC") or "", None),
                "carnegie_code": val(row, "CCBASIC"),
                "health_special_focus": (val(row, "CCBASIC") in SPECIAL_FOCUS_HEALTH),
                "scorecard": page,
                "profile": {
                    # Reported because applicants need them. Never scored: see
                    # build_colleges.py on why selectivity is left out of the score.
                    "admit_rate_pct": field(num(row, "ADM_RATE", float, 100.0, 1), page),
                    "sat_avg": field(num(row, "SAT_AVG", int), page),
                    "sat_reading_mid": field(num(row, "SATVRMID", int), page),
                    "sat_math_mid": field(num(row, "SATMTMID", int), page),
                    "act_mid": field(num(row, "ACTCMMID", int), page),
                    "test_policy": field(TEST_POLICY.get(val(row, "ADMCON7") or ""), page),
                    "undergrads": field(ug, page),
                    # Cost. Net price is what students actually pay after grant aid and
                    # is the honest number; sticker price is reported alongside it.
                    "net_price_usd": field(
                        num(row, "NPT4_PUB" if public else "NPT4_PRIV", int), page),
                    "cost_attendance_usd": field(num(row, "COSTT4_A", int), page),
                    "tuition_in_state_usd": field(num(row, "TUITIONFEE_IN", int), page),
                    "tuition_out_state_usd": field(num(row, "TUITIONFEE_OUT", int), page),
                    # Outcomes.
                    "grad_rate_6yr_pct": field(num(row, "C150_4", float, 100.0, 1), page),
                    "retention_pct": field(num(row, "RET_FT4", float, 100.0, 1), page),
                    "earnings_10yr_usd": field(num(row, "MD_EARN_WNE_P10", int), page),
                    "median_debt_usd": field(num(row, "GRAD_DEBT_MDN", int), page),
                    "pell_pct": field(num(row, "PCTPELL", float, 100.0, 1), page),
                    "federal_loan_pct": field(num(row, "PCTFLOAN", float, 100.0, 1), page),
                },
                # Institutional scholarship policy is not in the Scorecard. It is filled
                # in per school from the school's own aid page, the same source ladder the
                # MBA library uses, and stays null until it is.
                "scholarship": {
                    "pct_receiving": {"v": None},
                    "avg_award_usd": {"v": None},
                    "auto_considered": {"v": None},
                    "notes": None,
                },
            }
            (OUT / ("%s.json" % slug)).write_text(
                json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            made += 1
    print("wrote %d colleges to data/colleges/ (%d rows skipped by the filters)"
          % (made, skipped))
    return made


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    main(sys.argv[1])
