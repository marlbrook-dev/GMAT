"""College Board's SAT percentile tables, read from the page that prints them.

    python3 src/sat_percentiles.py --write   rebuild data/sat_percentiles.json from the sources
    python3 src/sat_percentiles.py --check   re-read the page and report any difference

The SAT score calculator shows College Board's nationally representative and user group
percentiles for every total and section score. They come from College Board's research
site, and the rule that the total is the sum of the two section scores comes from its
fall 2026 Understanding Scores guide. Nothing in the data file is typed: --write parses
the page's two tables, quotes each definition only if the page prints it word for word,
and takes the page's date from its Last-Modified header.

College Board revises the tables on its own schedule, as ETS revised the GRE fee
(INC-0132), so the weekly source job runs --check, which fails when a cell, a row or a
quoted definition no longer matches. Exit codes: 0 in step, 1 different, 2 unreadable.
"""
import email.utils
import html
import io
import json
import pathlib
import re
import sys
import urllib.request

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
from check_sources import UA, ssl_context, to_text

OUT = ROOT / "data" / "sat_percentiles.json"
PAGE = "https://research.collegeboard.org/reports/sat-suite/understanding-scores/sat"
GUIDE = "https://satsuite.collegeboard.org/media/pdf/sat-understanding-scores.pdf"
CELL = re.compile(r"^(99\+|1-|[1-9]\d?)$")
DEFINITIONS = {
    "rank": "A student's percentile rank represents the percentage of students with scores "
            "equal to or lower than their score.",
    "national": "Nationally representative percentiles are derived from a research study of "
                "U.S. students in 11th and 12th grade and are weighted to represent all U.S. "
                "students in those grades, regardless of whether they typically take the SAT.",
    "user": "User group percentiles are based on the actual SAT scores of students that "
            "graduated in the past three school years.",
}
# What the guide prints, as its text layer reads: a table row, then a sentence.
GUIDE_SUM = "Total Score Sum of the 2 section scores Score Range 200–800 200–800 400–1600"
GUIDE_TESTER = ("All Tester Percentiles are based on the actual scores of the past 3 cohorts of "
                "students who took the SAT in 12th grade for tests completed anywhere in the "
                "world.")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as r:
        return r.read(), r.headers.get("Content-Type", "").lower(), r.headers.get("Last-Modified")


def cells(table):
    rows = []
    for tr in re.findall(r"<tr.*?</tr>", table, flags=re.S):
        rows.append([re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                     for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.S)])
    return rows


def parse(page):
    """The two tables and the three definitions, or a list of what did not parse."""
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
    bad = []
    tables = re.findall(r"<table.*?</table>", body, flags=re.S)
    if len(tables) != 2:
        return None, ["expected two tables, found %d" % len(tables)]
    tot, sec = cells(tables[0]), cells(tables[1])
    if tot[0] != ["Total Score", "Nationally Representative Percentiles", "User Group Percentiles"]:
        bad.append("the total table's header changed: %r" % tot[0])
    if sec[:2] != [["", "Reading and Writing", "Math"],
                   ["Section Score", "Nationally Representative Percentiles", "User Group Percentiles",
                    "Nationally Representative Percentiles", "User Group Percentiles"]]:
        bad.append("the section table's header changed: %r" % sec[:2])
    data = {"total": {"national": {}, "user": {}}, "rw": {"national": {}, "user": {}},
            "math": {"national": {}, "user": {}}}
    for row in tot[1:]:
        if len(row) != 3 or not all(CELL.match(c) for c in row[1:]):
            bad.append("an unexpected total row: %r" % row)
            continue
        data["total"]["national"][row[0]], data["total"]["user"][row[0]] = row[1], row[2]
    for row in sec[2:]:
        if len(row) != 5 or not all(CELL.match(c) for c in row[1:]):
            bad.append("an unexpected section row: %r" % row)
            continue
        data["rw"]["national"][row[0]], data["rw"]["user"][row[0]] = row[1], row[2]
        data["math"]["national"][row[0]], data["math"]["user"][row[0]] = row[3], row[4]
    if list(data["total"]["national"]) != [str(s) for s in range(1600, 399, -10)]:
        bad.append("the totals are not every score from 1600 down to 400")
    if list(data["rw"]["national"]) != [str(s) for s in range(800, 199, -10)]:
        bad.append("the section scores are not every score from 800 down to 200")
    for k, quote in DEFINITIONS.items():
        if quote not in text:
            bad.append("the page no longer prints the %s definition word for word" % k)
    return data, bad


def write(read_date):
    page, _, modified = fetch(PAGE)
    data, bad = parse(page.decode("utf-8", errors="replace"))
    guide = re.sub(r"\s+", " ", to_text(*fetch(GUIDE)[:2]))
    for quote in (GUIDE_SUM, GUIDE_TESTER):
        if quote not in guide:
            bad.append("the guide no longer prints %r" % quote[:60])
    if bad or not modified:
        sys.exit("sat_percentiles: " + ("; ".join(bad) or "the page sent no Last-Modified date"))
    mod = email.utils.parsedate_to_datetime(modified).date().isoformat()
    out = {
        "what": "College Board's SAT percentile ranks: for every total and section score, the "
                "percentage of students in each of two groups with scores equal to or lower "
                "than it.",
        "src": "College Board", "year": int(read_date[:4]), "url": PAGE,
        "title": "SAT Nationally Representative and User Percentiles",
        "read": read_date, "modified": mod,
        "definitions": DEFINITIONS,
        **data,
        "sum_rule": {
            "text": "The total score is the sum of the two section scores: Reading and Writing "
                    "and Math, each 200 to 800, for a total of 400 to 1600",
            "src": "College Board", "year": 2026, "url": GUIDE,
            "title": "Fall 2026 SAT Weekend Understanding Scores"},
        "all_tester": {
            "text": GUIDE_TESTER, "src": "College Board", "year": 2026, "url": GUIDE,
            "title": "Fall 2026 SAT Weekend Understanding Scores"},
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("wrote %s: %d totals, %d section scores, page modified %s"
          % (OUT.relative_to(ROOT), len(data["total"]["national"]), len(data["rw"]["national"]), mod))


def check():
    have = json.loads(OUT.read_text())
    try:
        page = fetch(have["url"])[0].decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001 - any failure to read is reported, not raised
        print("could not read %s (%s: %s)" % (have["url"], type(e).__name__, e))
        return 2
    data, bad = parse(page)
    if data:
        for part in ("total", "rw", "math"):
            for grp in ("national", "user"):
                was, now = have[part][grp], data[part][grp]
                diff = [k for k in sorted(set(was) | set(now), key=int, reverse=True)
                        if was.get(k) != now.get(k)]
                if diff:
                    bad.append("%s %s percentiles changed at %d scores, e.g. %s: %s now %s"
                               % (part, grp, len(diff), diff[0], was.get(diff[0]), now.get(diff[0])))
    for line in bad:
        print(line)
    print("SAT percentile tables: %s" % ("changed on College Board's page; run "
          "python3 src/sat_percentiles.py --write and read the diff" if bad else "in step with College Board's page"))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--write" in sys.argv:
        import datetime
        write(datetime.date.today().isoformat())
    elif "--check" in sys.argv:
        sys.exit(check())
    else:
        sys.exit(__doc__)
