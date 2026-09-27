"""College Board's SAT and PSAT/NMSQT percentile tables, read from the pages that print them.

    python3 src/sat_percentiles.py --write   rebuild both data files from the sources
    python3 src/sat_percentiles.py --check   re-read both pages and report any difference

The SAT and PSAT/NMSQT score calculators show College Board's nationally representative
and user group percentiles for every total and section score. They come from College
Board's research site; the rule that the SAT total is the sum of the two section scores
comes from its fall 2026 Understanding Scores guide, and the PSAT/NMSQT score ranges and
the NMSC Selection Index rule from its What Do My Scores Mean? page. Nothing in either
data file is typed: --write parses the tables, quotes each definition and rule only if the
source prints it word for word, and takes each page's date from its Last-Modified header.

    data/sat_percentiles.json    the SAT: one table of totals, one of section scores
    data/psat_percentiles.json   the PSAT/NMSQT: totals by grade, then section scores for
                                 10th and then 11th grade, each table's grade read from
                                 the heading the page prints before it; with the scoring
                                 rules and grade-level benchmarks from its fall 2026 guide

College Board revises the tables on its own schedule, as ETS revised the GRE fee
(INC-0132), so the weekly source job runs --check, which fails when a cell, a row or a
quoted definition no longer matches. Exit codes: 0 in step, 1 different, 2 unreadable.
"""
import email.utils
import html
import json
import pathlib
import re
import sys
import urllib.request

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
from check_sources import UA, ssl_context, to_text

SAT_OUT = ROOT / "data" / "sat_percentiles.json"
PSAT_OUT = ROOT / "data" / "psat_percentiles.json"
PAGE = "https://research.collegeboard.org/reports/sat-suite/understanding-scores/sat"
PSAT_PAGE = "https://research.collegeboard.org/reports/sat-suite/understanding-scores/psat-nmsqt"
GUIDE = "https://satsuite.collegeboard.org/media/pdf/sat-understanding-scores.pdf"
PSAT_GUIDE = "https://satsuite.collegeboard.org/media/pdf/psat-nmsqt-understanding-scores.pdf"
SCORES = "https://satsuite.collegeboard.org/scores/what-scores-mean"
CELL = re.compile(r"^(99\+|1-|[1-9]\d?)$")
NR, UG = "Nationally Representative Percentiles", "User Group Percentiles"
RANK = ("A student's percentile rank represents the percentage of students with scores equal "
        "to or lower than their score.")
DEFINITIONS = {
    "rank": RANK,
    "national": "Nationally representative percentiles are derived from a research study of "
                "U.S. students in 11th and 12th grade and are weighted to represent all U.S. "
                "students in those grades, regardless of whether they typically take the SAT.",
    "user": "User group percentiles are based on the actual SAT scores of students that "
            "graduated in the past three school years.",
}
PSAT_DEFINITIONS = {
    "rank": RANK,
    "national": "Nationally representative percentiles are derived from a research study of "
                "U.S. students in the 10th or 11th grade and are weighted to represent all "
                "U.S. students in those grades, regardless of whether they typically take the "
                "PSAT/NMSQT or the PSAT 10.",
    "user": "User group percentiles are based on the actual scores of students who took the "
            "PSAT/NMSQT or the PSAT 10 in the past three school years.",
}
# What the sources print, as their text layers read. The guide's is a table row and then a
# sentence; the scores page's is a table of ranges by test and then the Selection Index.
GUIDE_SUM = "Total Score Sum of the 2 section scores Score Range 200–800 200–800 400–1600"
GUIDE_TESTER = ("All Tester Percentiles are based on the actual scores of the past 3 cohorts of "
                "students who took the SAT in 12th grade for tests completed anywhere in the "
                "world.")
GUIDE_SCALE = ("The SAT Suite—from the PSAT 8/9 through the SAT—uses a common score "
               "scale for the total and section scores.")
SCORES_RANGES = ("Assessment SAT SAT with Essay PSAT/NMSQT PSAT 10 PSAT 8/9 Total Score "
                 "400–1600 400–1600 320–1520 320–1520 240–1440 Section Scores "
                 "200–800 200–800 160–760 160–760 120–720")
SCORES_SI_SCALE = "NMSC Selection Index Score on a scale of 48–228"
SCORES_SI_ONLY = "NMSC Selection Index for PSAT/NMSQT only"
SCORES_SI_RULE = ("Your score is calculated by doubling your Reading and Writing Score, adding "
                  "it to your Math score, then dividing that sum by 10.")
# The PSAT/NMSQT guide's scoring table, its percentile rules and its grade-level benchmarks.
PSAT_GUIDE_TABLE = ("Section Scores (2) Reading and Writing (RW) Math (M) Total Score Sum of the 2 "
                    "section scores NMSC Selection Index Score 2RW + M 10 Score Range "
                    "160\u2013760 160\u2013760 320\u20131520 48\u2013228")
PSAT_GUIDE_TESTER = ("All Tester Percentiles are based on the actual scores of the past 3 cohorts "
                     "of students who took the PSAT/NMSQT in 10th or 11th grade, for tests "
                     "completed anywhere in the world.")
PSAT_GUIDE_GRADE = ("Students in 10th grade are provided the 10th-grade percentile, and students "
                    "in 11th grade are provided the 11th-grade percentile.")
PSAT_GUIDE_BENCH = re.compile(r"PSAT/NMSQT GRADE-LEVEL BENCHMARKS Reading and Writing 10th grade "
                              r"11th grade (\d{3}) (\d{3}) Math (\d{3}) (\d{3})")
PSAT_GUIDE_ON_TRACK = ("Students meeting or exceeding these benchmarks are considered on track to "
                       "be college ready.")


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


def plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment)))


def columns(rows, bad, what, keys, n):
    """[{score: cell}] for each of n percentile columns, checking every row as it goes."""
    out = [dict() for _ in range(n)]
    for row in rows:
        if len(row) != n + 1 or not all(CELL.match(c) for c in row[1:]):
            bad.append("an unexpected %s row: %r" % (what, row))
            continue
        for i in range(n):
            out[i][row[0]] = row[i + 1]
    if list(out[0]) != keys:
        bad.append("the %s rows are not every score from %s down to %s" % (what, keys[0], keys[-1]))
    return out


def scores(top, bottom):
    return [str(s) for s in range(top, bottom - 1, -10)]


def parse(page):
    """The SAT page's two tables and three definitions, or a list of what did not parse."""
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S)
    text = plain(body)
    bad = []
    tables = re.findall(r"<table.*?</table>", body, flags=re.S)
    if len(tables) != 2:
        return None, ["expected two tables, found %d" % len(tables)]
    tot, sec = cells(tables[0]), cells(tables[1])
    if tot[0] != ["Total Score", NR, UG]:
        bad.append("the total table's header changed: %r" % tot[0])
    if sec[:2] != [["", "Reading and Writing", "Math"], ["Section Score", NR, UG, NR, UG]]:
        bad.append("the section table's header changed: %r" % sec[:2])
    t = columns(tot[1:], bad, "total", scores(1600, 400), 2)
    s = columns(sec[2:], bad, "section", scores(800, 200), 4)
    data = {"total": {"national": t[0], "user": t[1]},
            "rw": {"national": s[0], "user": s[1]},
            "math": {"national": s[2], "user": s[3]}}
    for k, quote in DEFINITIONS.items():
        if quote not in text:
            bad.append("the page no longer prints the %s definition word for word" % k)
    return data, bad


def parse_psat(page):
    """The PSAT/NMSQT page's three tables and three definitions.

    Totals come in one table with a column pair per grade. Section scores come in two
    tables, and the page says which grade each is for only in a heading printed before it,
    so that heading is read rather than assumed from the order."""
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S)
    text = plain(body)
    bad = []
    parts = re.split(r"(<table.*?</table>)", body, flags=re.S)
    tables = parts[1::2]
    if len(tables) != 3:
        return None, ["expected three tables, found %d" % len(tables)]
    tot = cells(tables[0])
    if tot[:2] != [["", "10th Grade", "11th Grade"], ["Total Score", NR, UG, NR, UG]]:
        bad.append("the total table's header changed: %r" % tot[:2])
    t = columns(tot[2:], bad, "total", scores(1520, 320), 4)
    data = {"total": {"10": {"national": t[0], "user": t[1]}, "11": {"national": t[2], "user": t[3]}},
            "rw": {}, "math": {}, "rw_heading": {}}
    for i, grade in ((1, "10"), (2, "11")):
        before = plain(parts[2 * i])
        if "%sth Grade" % grade not in before or "Percentiles for Section Scores" not in before:
            bad.append("the heading before section table %d no longer names %sth grade" % (i, grade))
        sec = cells(tables[i])
        if len(sec) < 2 or len(sec[0]) != 3 or sec[0][2] != "Math" or sec[1] != ["Section Score", NR, UG, NR, UG]:
            bad.append("section table %d's header changed: %r" % (i, sec[:2]))
            continue
        s = columns(sec[2:], bad, "grade %s section" % grade, scores(760, 160), 4)
        data["rw"][grade] = {"national": s[0], "user": s[1]}
        data["math"][grade] = {"national": s[2], "user": s[3]}
        data["rw_heading"][grade] = sec[0][1]
    for k, quote in PSAT_DEFINITIONS.items():
        if quote not in text:
            bad.append("the page no longer prints the %s definition word for word" % k)
    return data, bad


def page_date(modified, bad):
    if not modified:
        bad.append("a page sent no Last-Modified date")
        return None
    return email.utils.parsedate_to_datetime(modified).date().isoformat()


def require(text, quotes, where, bad):
    for q in quotes:
        if q not in text:
            bad.append("%s no longer prints %r" % (where, q[:60]))


def write(read_date):
    bad = []
    page, _, modified = fetch(PAGE)
    data, more = parse(page.decode("utf-8", errors="replace"))
    bad += more
    mod = page_date(modified, bad)
    ppage, _, pmodified = fetch(PSAT_PAGE)
    pdata, more = parse_psat(ppage.decode("utf-8", errors="replace"))
    bad += more
    pmod = page_date(pmodified, bad)
    guide = re.sub(r"\s+", " ", to_text(*fetch(GUIDE)[:2]))
    require(guide, (GUIDE_SUM, GUIDE_TESTER, GUIDE_SCALE), "the Understanding Scores guide", bad)
    pguide = re.sub(r"\s+", " ", to_text(*fetch(PSAT_GUIDE)[:2]))
    require(pguide, ("Fall 2026 PSAT/NMSQT Understanding Scores", PSAT_GUIDE_TABLE, PSAT_GUIDE_TESTER,
                     PSAT_GUIDE_GRADE, PSAT_GUIDE_ON_TRACK), "the PSAT/NMSQT guide", bad)
    bench = PSAT_GUIDE_BENCH.search(pguide)
    if not bench:
        bad.append("the PSAT/NMSQT guide no longer prints its grade-level benchmark table")
    scores_page = plain(re.sub(r"<script.*?</script>|<style.*?</style>", " ",
                               fetch(SCORES)[0].decode("utf-8", errors="replace"), flags=re.S))
    require(scores_page, (SCORES_RANGES, SCORES_SI_SCALE, SCORES_SI_ONLY, SCORES_SI_RULE),
            "the What Do My Scores Mean? page", bad)
    if bad:
        sys.exit("sat_percentiles: " + "; ".join(bad))
    guide_ref = {"src": "College Board", "year": 2026, "url": GUIDE,
                 "title": "Fall 2026 SAT Weekend Understanding Scores"}
    scores_ref = {"src": "College Board", "year": int(read_date[:4]), "url": SCORES,
                  "title": "What Do My Scores Mean?"}
    pguide_ref = {"src": "College Board", "year": 2026, "url": PSAT_GUIDE,
                  "title": "Fall 2026 PSAT/NMSQT Understanding Scores"}
    sat = {
        "what": "College Board's SAT percentile ranks: for every total and section score, the "
                "percentage of students in each of two groups with scores equal to or lower "
                "than it.",
        "src": "College Board", "year": int(read_date[:4]), "url": PAGE,
        "title": "SAT Nationally Representative and User Percentiles",
        "read": read_date, "modified": mod,
        "definitions": DEFINITIONS,
        **data,
        "sum_rule": dict(text="The total score is the sum of the two section scores: Reading "
                              "and Writing and Math, each 200 to 800, for a total of 400 to 1600",
                         **guide_ref),
        "all_tester": dict(text=GUIDE_TESTER, **guide_ref),
    }
    psat = {
        "what": "College Board's PSAT/NMSQT percentile ranks: for every total and section score, "
                "the percentage of 10th and of 11th graders in each of two groups with scores "
                "equal to or lower than it.",
        "src": "College Board", "year": int(read_date[:4]), "url": PSAT_PAGE,
        "title": "PSAT/NMSQT Nationally Representative and User Percentiles",
        "read": read_date, "modified": pmod,
        "definitions": PSAT_DEFINITIONS,
        **pdata,
        "ranges": dict(text="Reading and Writing and Math are each scored 160 to 760, the total "
                            "is the sum of the two section scores, 320 to 1520, and the NMSC "
                            "Selection Index is twice Reading and Writing plus Math, over 10, "
                            "48 to 228", **pguide_ref),
        "selection_index": dict(text=SCORES_SI_RULE, scale="48 to 228", **scores_ref),
        "all_tester": dict(text=PSAT_GUIDE_TESTER + " " + PSAT_GUIDE_GRADE, **pguide_ref),
        "benchmarks": dict(rw={"10": int(bench.group(1)), "11": int(bench.group(2))},
                           math={"10": int(bench.group(3)), "11": int(bench.group(4))},
                           text=PSAT_GUIDE_ON_TRACK, **pguide_ref),
        "common_scale": dict(text="College Board says the SAT Suite, from the PSAT 8/9 through "
                                  "the SAT, uses a common score scale for the total and section "
                                  "scores", **guide_ref),
    }
    for out, d in ((SAT_OUT, sat), (PSAT_OUT, psat)):
        s = json.dumps(d, indent=1, ensure_ascii=False)
        if "—" in s or "–" in s:
            sys.exit("sat_percentiles: %s would carry a dash" % out.name)
        out.write_text(s + "\n")
    print("wrote %s: %d totals, %d section scores, page modified %s"
          % (SAT_OUT.relative_to(ROOT), len(data["total"]["national"]), len(data["rw"]["national"]), mod))
    print("wrote %s: %d totals and %d section scores for each of 2 grades, page modified %s"
          % (PSAT_OUT.relative_to(ROOT), len(pdata["total"]["10"]["national"]),
             len(pdata["rw"]["10"]["national"]), pmod))


def differences(was, now, where, bad):
    """Every percentile column in `was` compared with the same one in `now`."""
    for key in sorted(set(was) | set(now)):
        a, b = was.get(key), now.get(key)
        if isinstance(a, dict) and isinstance(b, dict) and not all(isinstance(v, str) for v in a.values()):
            differences(a, b, where + [key], bad)
        elif a != b:
            if isinstance(a, dict) and isinstance(b, dict):
                diff = [k for k in sorted(set(a) | set(b), key=int, reverse=True) if a.get(k) != b.get(k)]
                bad.append("%s changed at %d scores, e.g. %s: %s now %s"
                           % (" ".join(where + [key]), len(diff), diff[0], a.get(diff[0]), b.get(diff[0])))
            else:
                bad.append("%s changed: %r now %r" % (" ".join(where + [key]), a, b))


def check_one(out, parser, name):
    have = json.loads(out.read_text())
    try:
        page = fetch(have["url"])[0].decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001 - any failure to read is reported, not raised
        print("could not read %s (%s: %s)" % (have["url"], type(e).__name__, e))
        return 2
    data, bad = parser(page)
    if data:
        differences({k: have.get(k) for k in data}, data, [], bad)
    for line in bad:
        print("  " + line)
    print("%s percentile tables: %s" % (name, "changed on College Board's page; run python3 "
          "src/sat_percentiles.py --write and read the diff" if bad else "in step with College Board's page"))
    return 1 if bad else 0


def check():
    codes = [check_one(SAT_OUT, parse, "SAT"), check_one(PSAT_OUT, parse_psat, "PSAT/NMSQT")]
    return 1 if 1 in codes else 2 if 2 in codes else 0


if __name__ == "__main__":
    if "--write" in sys.argv:
        import datetime
        write(datetime.date.today().isoformat())
    elif "--check" in sys.argv:
        sys.exit(check())
    else:
        sys.exit(__doc__)
